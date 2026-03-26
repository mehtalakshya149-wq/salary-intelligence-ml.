"""
explainability.py — SHAP-Based Model Explanations
===================================================
Provides both global (dataset-wide) and local (single-prediction)
explanations using SHAP TreeExplainer.

Global explanations show which features matter most overall.
Local explanations show why a specific prediction was made.
"""

import os
import json
import logging
import argparse
import numpy as np
import pandas as pd
import joblib
import shap
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for server/Docker use
import matplotlib.pyplot as plt

from ml.src.preprocess import load_config

logger = logging.getLogger(__name__)


# ── Global SHAP ───────────────────────────────────────────

def compute_global_shap(
    model,
    X_train: pd.DataFrame,
    max_samples: int = 500,
) -> tuple[np.ndarray, shap.Explainer]:
    """
    Compute global SHAP values across the training set.

    Uses TreeExplainer for fast, exact SHAP computation on
    tree-based models (RF, GB).

    Args:
        model: Fitted tree-based model.
        X_train: Training feature DataFrame.
        max_samples: Max rows to explain (subsample for speed).

    Returns:
        Tuple of (shap_values array, fitted explainer).
    """
    # Subsample if dataset is large
    if len(X_train) > max_samples:
        X_sample = X_train.sample(n=max_samples, random_state=42)
        logger.info(f"Subsampled {max_samples}/{len(X_train)} rows for SHAP")
    else:
        X_sample = X_train

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    logger.info(f"Global SHAP computed -- shape: {shap_values.shape}")
    return shap_values, explainer


def get_feature_importance(
    shap_values: np.ndarray, feature_names: list[str]
) -> dict:
    """
    Compute mean absolute SHAP value per feature (global importance).

    Args:
        shap_values: SHAP values array (n_samples × n_features).
        feature_names: List of feature names.

    Returns:
        Dict of {feature_name: mean_abs_shap}, sorted descending.
    """
    mean_abs = np.abs(shap_values).mean(axis=0)
    importance = dict(zip(feature_names, [round(float(v), 4) for v in mean_abs]))
    importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
    logger.info(f"Top 3 features: {list(importance.keys())[:3]}")
    return importance


# ── Local SHAP ────────────────────────────────────────────

def compute_local_shap(
    model,
    X_single: pd.DataFrame,
    X_background: pd.DataFrame,
    max_background: int = 100,
) -> dict:
    """
    Compute SHAP values for a single prediction to explain
    why the model predicted a specific salary.

    Args:
        model: Fitted tree-based model.
        X_single: Single-row DataFrame to explain.
        X_background: Background dataset for the explainer.
        max_background: Max background samples.

    Returns:
        Dict with base_value, feature contributions, and predicted value.
    """
    # Subsample background
    if len(X_background) > max_background:
        X_bg = X_background.sample(n=max_background, random_state=42)
    else:
        X_bg = X_background

    explainer = shap.TreeExplainer(model, X_bg)
    shap_values = explainer.shap_values(X_single)

    # Build feature contribution dict
    feature_names = list(X_single.columns)
    contributions = {}
    for name, value in zip(feature_names, shap_values[0]):
        contributions[name] = round(float(value), 2)

    # Sort by absolute contribution
    contributions = dict(
        sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    )

    base_value = float(explainer.expected_value)
    predicted = base_value + sum(shap_values[0])

    result = {
        "base_value": round(base_value, 2),
        "contributions": contributions,
        "predicted_value": round(predicted, 2),
    }

    logger.info(
        f"Local SHAP -- base: {result['base_value']}, "
        f"predicted: {result['predicted_value']}"
    )
    return result


# ── Visualization ─────────────────────────────────────────

def generate_shap_summary_plot(
    shap_values: np.ndarray,
    X_data: pd.DataFrame,
    save_path: str,
) -> str:
    """
    Generate and save a SHAP beeswarm summary plot.
    Shows the distribution of SHAP values per feature.

    Args:
        shap_values: Global SHAP values array.
        X_data: Feature DataFrame matching shap_values.
        save_path: Directory to save the plot.

    Returns:
        Path to the saved PNG file.
    """
    os.makedirs(save_path, exist_ok=True)
    filepath = os.path.join(save_path, "shap_summary.png")

    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X_data, show=False)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"SHAP summary plot saved -> {filepath}")
    return filepath


def generate_shap_bar_plot(
    shap_values: np.ndarray,
    feature_names: list[str],
    save_path: str,
) -> str:
    """
    Generate and save a SHAP bar chart (mean |SHAP| per feature).

    Args:
        shap_values: Global SHAP values array.
        feature_names: List of feature names.
        save_path: Directory to save the plot.

    Returns:
        Path to the saved PNG file.
    """
    os.makedirs(save_path, exist_ok=True)
    filepath = os.path.join(save_path, "shap_bar.png")

    mean_abs = np.abs(shap_values).mean(axis=0)
    sorted_idx = np.argsort(mean_abs)[::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(
        range(len(sorted_idx)),
        mean_abs[sorted_idx],
        color="#6C63FF",
        edgecolor="white",
    )
    plt.yticks(
        range(len(sorted_idx)),
        [feature_names[i] for i in sorted_idx],
    )
    plt.xlabel("Mean |SHAP Value|")
    plt.title("Feature Importance (SHAP)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"SHAP bar plot saved -> {filepath}")
    return filepath


def generate_shap_waterfall(
    base_value: float,
    shap_values: np.ndarray,
    feature_names: list[str],
    save_path: str,
) -> str:
    """
    Generate and save a SHAP waterfall plot for a single prediction.
    Shows how each feature pushes the prediction up or down.

    Args:
        base_value: Model's expected value (average prediction).
        shap_values: SHAP values for a single sample (1D array).
        feature_names: List of feature names.
        save_path: Directory to save the plot.

    Returns:
        Path to the saved PNG file.
    """
    os.makedirs(save_path, exist_ok=True)
    filepath = os.path.join(save_path, "shap_waterfall.png")

    explanation = shap.Explanation(
        values=shap_values,
        base_values=base_value,
        feature_names=feature_names,
    )

    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(explanation, show=False)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()

    logger.info(f"SHAP waterfall plot saved -> {filepath}")
    return filepath


# ── End-to-End Explainability ─────────────────────────────

def run_explainability(config_path: str = "ml/config.yaml") -> dict:
    """
    Full explainability pipeline:
    1. Load RF model and training/test data
    2. Compute global SHAP values
    3. Generate feature importance ranking
    4. Save summary + bar plots
    5. Save importance JSON

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Dict with importance ranking and plot paths.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    config = load_config(config_path)
    model_dir = config["paths"]["model_dir"]
    meta_dir = config["paths"]["metadata_dir"]
    shap_dir = config["paths"]["shap_dir"]

    # Load RF model (used for SHAP — cleaner explanations than ensemble)
    rf_model = joblib.load(os.path.join(model_dir, "random_forest.joblib"))

    # Load test data for SHAP background
    test_data = joblib.load(os.path.join(model_dir, "test_data.joblib"))
    X_test = test_data["X_test"]

    # Global SHAP
    shap_values, explainer = compute_global_shap(rf_model, X_test)
    feature_names = list(X_test.columns)
    importance = get_feature_importance(shap_values, feature_names)

    # Save importance JSON
    os.makedirs(meta_dir, exist_ok=True)
    importance_path = os.path.join(meta_dir, "feature_importance.json")
    with open(importance_path, "w", encoding="utf-8") as f:
        json.dump(importance, f, indent=2)
    logger.info(f"Feature importance saved -> {importance_path}")

    # Generate plots
    summary_path = generate_shap_summary_plot(shap_values, X_test, shap_dir)
    bar_path = generate_shap_bar_plot(shap_values, feature_names, shap_dir)

    return {
        "feature_importance": importance,
        "plots": {
            "summary": summary_path,
            "bar": bar_path,
        },
        "importance_json": importance_path,
    }


# ── CLI Entry Point ───────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SHAP explanations")
    parser.add_argument(
        "--config", default="ml/config.yaml", help="Path to config YAML"
    )
    args = parser.parse_args()

    result = run_explainability(args.config)
    print("\n🔍 SHAP Explainability Results:")
    print("   Feature Importance (top 5):")
    for i, (feat, val) in enumerate(result["feature_importance"].items()):
        if i >= 5:
            break
        print(f"     {i+1}. {feat}: {val}")
    print(f"\n   Plots saved to: {result['plots']['summary']}")
