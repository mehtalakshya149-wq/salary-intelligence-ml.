"""
train.py — Model Training Pipeline
====================================
Trains RandomForestRegressor and GradientBoostingRegressor,
wraps them in a VotingRegressor ensemble, and saves all
artifacts (models, feature list, metadata) to disk.
"""

import os
import json
import logging
import argparse
import numpy as np
import pandas as pd
import joblib
import yaml
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    VotingRegressor,
)
from sklearn.model_selection import train_test_split, cross_val_score

from ml.src.preprocess import build_pipeline, load_config
from ml.src.feature_engineering import engineer_features

logger = logging.getLogger(__name__)


# ── Individual Model Training ─────────────────────────────

def train_random_forest(
    X: pd.DataFrame, y: pd.Series, params: dict
) -> RandomForestRegressor:
    """
    Train a RandomForestRegressor with config-driven hyperparameters.

    Args:
        X: Feature matrix.
        y: Target vector.
        params: Hyperparameter dict from config.yaml.

    Returns:
        Fitted RandomForestRegressor.
    """
    model = RandomForestRegressor(**params)
    model.fit(X, y)
    logger.info(
        f"RandomForest trained -- "
        f"n_estimators={params['n_estimators']}, "
        f"max_depth={params['max_depth']}"
    )
    return model


def train_gradient_boosting(
    X: pd.DataFrame, y: pd.Series, params: dict
) -> GradientBoostingRegressor:
    """
    Train a GradientBoostingRegressor with config-driven hyperparameters.

    Args:
        X: Feature matrix.
        y: Target vector.
        params: Hyperparameter dict from config.yaml.

    Returns:
        Fitted GradientBoostingRegressor.
    """
    model = GradientBoostingRegressor(**params)
    model.fit(X, y)
    logger.info(
        f"GradientBoosting trained -- "
        f"n_estimators={params['n_estimators']}, "
        f"learning_rate={params['learning_rate']}"
    )
    return model


# ── Ensemble Training ─────────────────────────────────────

def train_ensemble(
    X: pd.DataFrame, y: pd.Series, config: dict
) -> tuple[VotingRegressor, RandomForestRegressor, GradientBoostingRegressor]:
    """
    Train both models and combine them in a VotingRegressor.

    The VotingRegressor averages predictions using configurable
    weights, giving us the benefits of both model types:
    - RF: robust, handles noise, provides per-tree predictions for CI
    - GB: better at capturing complex non-linear patterns

    Individual models are also returned for SHAP analysis and
    percentile estimation from RF tree predictions.

    Args:
        X: Feature matrix.
        y: Target vector.
        config: Full parsed config dict.

    Returns:
        Tuple of (ensemble, rf_model, gb_model).
    """
    rf_params = config["models"]["random_forest"]
    gb_params = config["models"]["gradient_boosting"]
    weights_cfg = config["ensemble"]["weights"]

    # Train individual models
    rf_model = train_random_forest(X, y, rf_params)
    gb_model = train_gradient_boosting(X, y, gb_params)

    # Build ensemble
    weights = [weights_cfg["random_forest"], weights_cfg["gradient_boosting"]]
    ensemble = VotingRegressor(
        estimators=[
            ("rf", rf_model),
            ("gb", gb_model),
        ],
        weights=weights,
    )

    # VotingRegressor needs to be fit, but since sub-models are
    # already trained, we fit it to align the internal state
    ensemble.fit(X, y)

    logger.info(f"Ensemble trained -- weights: RF={weights[0]}, GB={weights[1]}")
    return ensemble, rf_model, gb_model


# ── Cross-Validation ──────────────────────────────────────

def cross_validate_model(
    model, X: pd.DataFrame, y: pd.Series, n_folds: int = 5
) -> dict:
    """
    Run k-fold cross-validation and return summary statistics.

    Args:
        model: Scikit-learn estimator (unfitted copy will be used).
        X: Feature matrix.
        y: Target vector.
        n_folds: Number of CV folds.

    Returns:
        Dict with cv_mean, cv_std, cv_scores.
    """
    scores = cross_val_score(
        model, X, y,
        cv=n_folds,
        scoring="r2",
        n_jobs=-1,
    )
    result = {
        "cv_r2_mean": round(float(np.mean(scores)), 4),
        "cv_r2_std": round(float(np.std(scores)), 4),
        "cv_r2_scores": [round(float(s), 4) for s in scores],
    }
    logger.info(f"CV R2 = {result['cv_r2_mean']} +/- {result['cv_r2_std']}")
    return result


# ── Model Saving ──────────────────────────────────────────

def save_model(model, path: str, name: str) -> str:
    """
    Serialize a model to disk using joblib.

    Args:
        model: Fitted scikit-learn model.
        path: Directory to save into.
        name: Filename (without extension).

    Returns:
        Full path to the saved file.
    """
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f"{name}.joblib")
    joblib.dump(model, filepath)
    logger.info(f"Model saved -> {filepath}")
    return filepath


# ── End-to-End Training ───────────────────────────────────

def run_training(config_path: str = "ml/config.yaml") -> dict:
    """
    Full training pipeline:
    1. Preprocess data (clean, encode, scale)
    2. Engineer features
    3. Train/test split
    4. Train ensemble (RF + GB)
    5. Cross-validate
    6. Save models + metadata

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Dict with model paths and training metadata.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    # Step 1: Preprocess
    X, y, config = build_pipeline(config_path)

    # Step 2: Feature engineering
    X = engineer_features(X, config)

    # Step 3: Train/test split
    train_cfg = config["training"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=train_cfg["test_size"],
        random_state=train_cfg["random_state"],
    )
    logger.info(f"Split -- Train: {X_train.shape}, Test: {X_test.shape}")

    # Step 4: Train ensemble
    ensemble, rf_model, gb_model = train_ensemble(X_train, y_train, config)

    # Step 5: Cross-validate (on training set)
    cv_results = cross_validate_model(
        RandomForestRegressor(**config["models"]["random_forest"]),
        X_train, y_train,
        n_folds=train_cfg["cross_validation_folds"],
    )

    # Step 6: Save models
    model_dir = config["paths"]["model_dir"]
    save_model(ensemble, model_dir, "ensemble")
    save_model(rf_model, model_dir, "random_forest")
    save_model(gb_model, model_dir, "gradient_boosting")

    # Save feature list for inference-time validation
    feature_list = list(X_train.columns)
    meta_dir = config["paths"]["metadata_dir"]
    os.makedirs(meta_dir, exist_ok=True)
    features_path = os.path.join(meta_dir, "feature_list.json")
    with open(features_path, "w", encoding="utf-8") as f:
        json.dump(feature_list, f, indent=2)
    logger.info(f"Feature list saved -> {features_path}")

    # Save training metadata
    metadata = {
        "n_train_samples": len(X_train),
        "n_test_samples": len(X_test),
        "n_features": len(feature_list),
        "feature_names": feature_list,
        "cross_validation": cv_results,
        "ensemble_weights": config["ensemble"]["weights"],
    }
    meta_path = os.path.join(meta_dir, "training_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Training metadata saved -> {meta_path}")

    # Save test set for evaluation
    test_path = os.path.join(model_dir, "test_data.joblib")
    joblib.dump({"X_test": X_test, "y_test": y_test}, test_path)
    logger.info(f"Test data saved -> {test_path}")

    return {
        "model_dir": model_dir,
        "metadata": metadata,
        "test_split": {"X_test_shape": X_test.shape, "y_test_shape": y_test.shape},
    }


# ── CLI Entry Point ───────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train salary prediction models")
    parser.add_argument(
        "--config", default="ml/config.yaml", help="Path to config YAML"
    )
    args = parser.parse_args()

    result = run_training(args.config)
    print("\nTraining complete!")
    print(f"   Models saved to: {result['model_dir']}")
    print(f"   Features: {result['metadata']['n_features']}")
    print(f"   CV R2: {result['metadata']['cross_validation']['cv_r2_mean']}")
