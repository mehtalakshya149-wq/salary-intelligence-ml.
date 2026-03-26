"""
predict.py — Salary Prediction & Confidence Scoring
=====================================================
Handles inference for both single and batch predictions.
Provides average, min (10th pctl), max (90th pctl) salary
estimates, confidence scores, and inflation adjustment.
"""

import os
import json
import logging
import numpy as np
import pandas as pd
import joblib

from ml.src.preprocess import load_config
from ml.src.feature_engineering import engineer_features

logger = logging.getLogger(__name__)


# ── Model & Encoder Loading ───────────────────────────────

def load_model(model_dir: str, name: str = "ensemble"):
    """
    Load a serialized model from disk.

    Args:
        model_dir: Directory containing model files.
        name: Model name (without extension).

    Returns:
        Deserialized scikit-learn model.
    """
    path = os.path.join(model_dir, f"{name}.joblib")
    model = joblib.load(path)
    logger.info(f"Loaded model from {path}")
    return model


def load_encoders(config: dict) -> dict:
    """
    Load fitted encoder and scaler from disk.

    Args:
        config: Parsed config dict with paths.

    Returns:
        Dict with 'encoder' and 'scaler' objects.
    """
    encoders = {}

    encoder_path = config["paths"]["encoder_path"]
    if os.path.exists(encoder_path):
        encoders["encoder"] = joblib.load(encoder_path)
        logger.info(f"Loaded encoder from {encoder_path}")

    scaler_path = config["paths"]["scaler_path"]
    if os.path.exists(scaler_path):
        encoders["scaler"] = joblib.load(scaler_path)
        logger.info(f"Loaded scaler from {scaler_path}")

    return encoders


def load_feature_list(meta_dir: str) -> list[str]:
    """
    Load the feature list that was used during training.
    This ensures inference uses the exact same feature order.

    Args:
        meta_dir: Metadata directory path.

    Returns:
        List of feature names.
    """
    path = os.path.join(meta_dir, "feature_list.json")
    with open(path, "r", encoding="utf-8") as f:
        features = json.load(f)
    logger.info(f"Loaded {len(features)} features from {path}")
    return features


# ── Input Preprocessing ───────────────────────────────────

def preprocess_input(
    raw_input: dict,
    config: dict,
    encoders: dict,
) -> pd.DataFrame:
    """
    Transform a single raw input dict into a model-ready DataFrame.

    Steps:
    1. Convert dict → single-row DataFrame
    2. Normalize string fields (strip, lowercase)
    3. Apply fitted encoder on categorical columns
    4. Apply fitted scaler on numeric columns
    5. Run feature engineering
    6. Align columns with training feature list

    Args:
        raw_input: Dict with feature names as keys.
        config: Parsed config dict.
        encoders: Dict with fitted 'encoder' and 'scaler'.

    Returns:
        Model-ready DataFrame (single row).
    """
    # Convert to DataFrame
    df = pd.DataFrame([raw_input])

    # Normalize strings
    for col in config["features"]["categorical"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    # Encode categoricals
    cat_cols = [c for c in config["features"]["categorical"] if c in df.columns]
    if "encoder" in encoders and cat_cols:
        df[cat_cols] = encoders["encoder"].transform(df[cat_cols])

    # Scale numerics
    num_cols = [c for c in config["features"]["numeric"] if c in df.columns]
    if "scaler" in encoders and num_cols:
        df[num_cols] = encoders["scaler"].transform(df[num_cols])

    # Feature engineering
    df = engineer_features(df, config)

    # Align with training features
    feature_list = load_feature_list(config["paths"]["metadata_dir"])
    for col in feature_list:
        if col not in df.columns:
            df[col] = 0  # Fill missing engineered features with 0
    df = df[feature_list]

    # Ensure no NaN values remain (can happen with single-row feature engineering)
    df = df.fillna(0)

    return df


# ── Salary Prediction ─────────────────────────────────────

def predict_salary(
    rf_model,
    ensemble_model,
    X: pd.DataFrame,
    config: dict,
) -> dict:
    """
    Generate salary predictions with range estimates.

    Uses individual tree predictions from the RandomForest to
    compute percentile-based salary ranges:
    - Average: ensemble prediction (weighted RF + GB)
    - Minimum: 10th percentile of RF tree predictions
    - Maximum: 90th percentile of RF tree predictions

    Args:
        rf_model: Fitted RandomForestRegressor.
        ensemble_model: Fitted VotingRegressor.
        X: Model-ready feature DataFrame.
        config: Parsed config dict.

    Returns:
        Dict with average, min, max salary estimates.
    """
    # Ensemble prediction (weighted average of RF + GB)
    avg_salary = float(ensemble_model.predict(X)[0])

    # Per-tree predictions from RF for range estimation
    tree_predictions = np.array([
        tree.predict(X)[0] for tree in rf_model.estimators_
    ])

    pctl_low = config["prediction"]["percentile_low"]
    pctl_high = config["prediction"]["percentile_high"]

    min_salary = float(np.percentile(tree_predictions, pctl_low))
    max_salary = float(np.percentile(tree_predictions, pctl_high))

    # Ensure logical ordering
    min_salary = min(min_salary, avg_salary)
    max_salary = max(max_salary, avg_salary)

    return {
        "average": round(avg_salary, 2),
        "min": round(min_salary, 2),
        "max": round(max_salary, 2),
    }


# ── Confidence Score ──────────────────────────────────────

def compute_confidence(rf_model, X: pd.DataFrame, config: dict) -> dict:
    """
    Compute a confidence score (0–100) for the prediction.

    Logic:
    - Collect predictions from all RF trees
    - Compute coefficient of variation (CV = std / mean)
    - Map CV to confidence: lower spread → higher confidence
    - Score = max(0, 100 - (CV * 200))

    Args:
        rf_model: Fitted RandomForestRegressor.
        X: Model-ready feature DataFrame.
        config: Parsed config dict.

    Returns:
        Dict with score (0–100) and label (High/Medium/Low).
    """
    tree_predictions = np.array([
        tree.predict(X)[0] for tree in rf_model.estimators_
    ])

    mean_pred = np.mean(tree_predictions)
    std_pred = np.std(tree_predictions)

    # Coefficient of variation
    cv = std_pred / mean_pred if mean_pred != 0 else 1.0

    # Map to 0–100 scale (lower CV → higher confidence)
    score = max(0, min(100, 100 - (cv * 200)))
    score = round(score, 1)

    # Assign label based on thresholds
    thresholds = config["prediction"]["confidence"]
    if score >= thresholds["high_threshold"]:
        label = "High"
    elif score >= thresholds["medium_threshold"]:
        label = "Medium"
    else:
        label = "Low"

    return {
        "score": score,
        "label": label,
        "std_deviation": round(float(std_pred), 2),
        "coefficient_of_variation": round(float(cv), 4),
    }


# ── Inflation Adjustment ─────────────────────────────────

def adjust_for_inflation(
    salary: float,
    work_year: int,
    config: dict,
) -> dict:
    """
    Adjust a salary from its work_year to the base year using
    cumulative CPI-based inflation rates from config.

    Example: A 2022 salary is adjusted forward to 2026 by
    compounding the inflation rates for 2023–2026.

    Args:
        salary: Original salary in USD.
        work_year: Year the salary corresponds to.
        config: Parsed config dict with inflation rates.

    Returns:
        Dict with original, adjusted salary, and multiplier.
    """
    inflation_cfg = config["inflation"]
    base_year = inflation_cfg["base_year"]
    rates = inflation_cfg["rates"]

    if work_year >= base_year:
        # No adjustment needed for current or future years
        return {
            "original": round(salary, 2),
            "adjusted": round(salary, 2),
            "multiplier": 1.0,
            "base_year": base_year,
        }

    # Compound inflation from work_year+1 to base_year
    multiplier = 1.0
    for year in range(work_year + 1, base_year + 1):
        rate = rates.get(year, 0.0) / 100.0  # Convert percentage to decimal
        multiplier *= (1 + rate)

    adjusted = salary * multiplier

    return {
        "original": round(salary, 2),
        "adjusted": round(adjusted, 2),
        "multiplier": round(multiplier, 4),
        "base_year": base_year,
    }


# ── End-to-End Prediction ─────────────────────────────────

def run_prediction(
    input_dict: dict,
    config_path: str = "ml/config.yaml",
) -> dict:
    """
    Full inference pipeline for a single input:
    1. Load config, models, encoders
    2. Preprocess input
    3. Predict salary (avg, min, max)
    4. Compute confidence score
    5. Apply inflation adjustment
    6. Return JSON-ready result

    Args:
        input_dict: Raw feature dict from API request.
        config_path: Path to the YAML config file.

    Returns:
        Complete prediction result dict.
    """
    config = load_config(config_path)

    # Load artifacts
    model_dir = config["paths"]["model_dir"]
    rf_model = load_model(model_dir, "random_forest")
    ensemble = load_model(model_dir, "ensemble")
    encoders = load_encoders(config)

    # Preprocess
    X = preprocess_input(input_dict, config, encoders)

    # Predict
    salary = predict_salary(rf_model, ensemble, X, config)

    # Confidence
    confidence = compute_confidence(rf_model, X, config)

    # Inflation adjustment
    work_year = int(input_dict.get("work_year", config["inflation"]["base_year"]))
    inflation = adjust_for_inflation(salary["average"], work_year, config)

    return {
        "salary": salary,
        "confidence": confidence,
        "inflation_adjusted": inflation,
        "input_features": input_dict,
    }
