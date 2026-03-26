"""
evaluate.py — Model Evaluation, Bias & Drift Detection
========================================================
Computes standard regression metrics, detects bias across
demographic groups, and checks for model drift over time.
"""

import os
import json
import logging
import argparse
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
)

from ml.src.preprocess import load_config

logger = logging.getLogger(__name__)


# ── Core Metrics ──────────────────────────────────────────

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Compute standard regression metrics.

    Args:
        y_true: Actual target values.
        y_pred: Predicted target values.

    Returns:
        Dict with MAE, RMSE, R², and MAPE.
    """
    metrics = {
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 2),
        "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_pred))), 2),
        "r2": round(float(r2_score(y_true, y_pred)), 4),
        "mape": round(float(mean_absolute_percentage_error(y_true, y_pred)) * 100, 2),
        "n_samples": len(y_true),
    }
    logger.info(
        f"Metrics -- MAE: {metrics['mae']}, RMSE: {metrics['rmse']}, "
        f"R2: {metrics['r2']}, MAPE: {metrics['mape']}%"
    )
    return metrics


# ── Bias Detection ────────────────────────────────────────

def detect_bias(
    df: pd.DataFrame,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    group_col: str,
    max_gap: float = 0.15,
) -> dict:
    """
    Detect prediction bias across subgroups (e.g., by region or
    company size). Flags if the R² gap between the best and worst
    performing group exceeds the configured threshold.

    Args:
        df: DataFrame with group column (pre-encoded or raw).
        y_true: Actual values.
        y_pred: Predicted values.
        group_col: Column name to group by.
        max_gap: Maximum allowable R² gap before flagging.

    Returns:
        Dict with per-group metrics, gap, and bias_flagged boolean.
    """
    if group_col not in df.columns:
        logger.warning(f"Bias detection skipped -- '{group_col}' not in DataFrame")
        return {"group_column": group_col, "skipped": True}

    # Bind predictions to a working DataFrame
    work_df = df[[group_col]].copy()
    work_df["y_true"] = y_true
    work_df["y_pred"] = y_pred

    group_metrics = {}
    for group_val, group_df in work_df.groupby(group_col):
        if len(group_df) < 5:
            continue  # Skip groups too small for meaningful R²
        gt = group_df["y_true"].values
        gp = group_df["y_pred"].values
        group_metrics[str(group_val)] = {
            "r2": round(float(r2_score(gt, gp)), 4) if len(set(gt)) > 1 else None,
            "mae": round(float(mean_absolute_error(gt, gp)), 2),
            "n_samples": len(group_df),
        }

    # Compute gap
    r2_values = [m["r2"] for m in group_metrics.values() if m["r2"] is not None]
    if len(r2_values) >= 2:
        gap = float(max(r2_values) - min(r2_values))
        bias_flagged = bool(gap > max_gap)
    else:
        gap = 0.0
        bias_flagged = False

    result = {
        "group_column": group_col,
        "group_metrics": group_metrics,
        "r2_gap": round(gap, 4),
        "max_allowed_gap": max_gap,
        "bias_flagged": bias_flagged,
    }

    if bias_flagged:
        logger.warning(
            f"BIAS DETECTED on '{group_col}' -- "
            f"R2 gap={gap:.4f} > threshold={max_gap}"
        )
    else:
        logger.info(f"Bias check passed for '{group_col}' -- gap={gap:.4f}")

    return result


# ── Drift Detection ───────────────────────────────────────

def detect_drift(
    df: pd.DataFrame,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    year_col: str = "work_year",
    r2_drop_threshold: float = 0.10,
) -> dict:
    """
    Check for model performance drift across years.
    Flags if the latest year's R² drops significantly compared
    to the average of prior years.

    This monitors temporal stability — if salary patterns shift
    (e.g., post-pandemic remote work changes), the model may
    underperform on newer data.

    Args:
        df: DataFrame with year column.
        y_true: Actual values.
        y_pred: Predicted values.
        year_col: Name of the year column.
        r2_drop_threshold: Max allowable R² drop.

    Returns:
        Dict with per-year R², drop magnitude, and drift_flagged.
    """
    if year_col not in df.columns:
        logger.warning(f"Drift detection skipped -- '{year_col}' not in DataFrame")
        return {"year_column": year_col, "skipped": True}

    work_df = df[[year_col]].copy()
    work_df["y_true"] = y_true
    work_df["y_pred"] = y_pred

    yearly_r2 = {}
    for year, year_df in work_df.groupby(year_col):
        if len(year_df) < 5:
            continue
        gt = year_df["y_true"].values
        gp = year_df["y_pred"].values
        if len(set(gt)) > 1:
            yearly_r2[str(year)] = round(float(r2_score(gt, gp)), 4)

    # Compute drift
    if len(yearly_r2) >= 2:
        sorted_years = sorted(yearly_r2.keys())
        latest_year = sorted_years[-1]
        prior_years = sorted_years[:-1]
        prior_avg = float(np.mean([yearly_r2[y] for y in prior_years]))
        latest_r2 = yearly_r2[latest_year]
        drop = float(prior_avg - latest_r2)
        drift_flagged = bool(drop > r2_drop_threshold)
    else:
        prior_avg = None
        latest_r2 = None
        drop = 0.0
        drift_flagged = False

    result = {
        "year_column": year_col,
        "yearly_r2": yearly_r2,
        "prior_avg_r2": round(float(prior_avg), 4) if prior_avg is not None else None,
        "latest_r2": latest_r2,
        "r2_drop": round(float(drop), 4),
        "drop_threshold": r2_drop_threshold,
        "drift_flagged": drift_flagged,
    }

    if drift_flagged:
        logger.warning(
            f"DRIFT DETECTED -- R2 drop={drop:.4f} > "
            f"threshold={r2_drop_threshold}"
        )
    else:
        logger.info(f"Drift check passed -- R2 drop={drop:.4f}")

    return result


# ── Report Generation ─────────────────────────────────────

def generate_report(
    metrics: dict,
    bias_reports: list[dict],
    drift_report: dict,
    save_dir: str,
) -> str:
    """
    Assemble and save a full evaluation report as JSON.

    Args:
        metrics: Core regression metrics dict.
        bias_reports: List of bias detection results.
        drift_report: Drift detection result.
        save_dir: Directory to save the report.

    Returns:
        Path to the saved report file.
    """
    report = {
        "overall_metrics": metrics,
        "bias_detection": bias_reports,
        "drift_detection": drift_report,
    }

    os.makedirs(save_dir, exist_ok=True)
    report_path = os.path.join(save_dir, "evaluation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Evaluation report saved -> {report_path}")
    return report_path


# ── End-to-End Evaluation ─────────────────────────────────

def run_evaluation(config_path: str = "ml/config.yaml") -> dict:
    """
    Full evaluation pipeline:
    1. Load config, test data, and trained model
    2. Generate predictions
    3. Compute core metrics
    4. Run bias detection on each configured group column
    5. Run drift detection
    6. Save evaluation report

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Complete evaluation report dict.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    config = load_config(config_path)

    # Load model and test data
    model_dir = config["paths"]["model_dir"]
    ensemble_path = os.path.join(model_dir, "ensemble.joblib")
    test_path = os.path.join(model_dir, "test_data.joblib")

    ensemble = joblib.load(ensemble_path)
    test_data = joblib.load(test_path)
    X_test = test_data["X_test"]
    y_test = test_data["y_test"]

    logger.info(f"Loaded ensemble from {ensemble_path}")
    logger.info(f"Test set: {X_test.shape}")

    # Predictions
    y_pred = ensemble.predict(X_test)

    # Core metrics
    metrics = compute_metrics(y_test.values, y_pred)

    # Bias detection
    bias_cfg = config.get("bias", {})
    bias_reports = []
    for group_col in bias_cfg.get("group_columns", []):
        bias_report = detect_bias(
            X_test, y_test.values, y_pred,
            group_col=group_col,
            max_gap=bias_cfg.get("max_metric_gap", 0.15),
        )
        bias_reports.append(bias_report)

    # Drift detection
    drift_cfg = config.get("drift", {})
    drift_report = detect_drift(
        X_test, y_test.values, y_pred,
        year_col=drift_cfg.get("year_column", "work_year"),
        r2_drop_threshold=drift_cfg.get("r2_drop_threshold", 0.10),
    )

    # Save report
    meta_dir = config["paths"]["metadata_dir"]
    report_path = generate_report(metrics, bias_reports, drift_report, meta_dir)

    return {
        "overall_metrics": metrics,
        "bias_detection": bias_reports,
        "drift_detection": drift_report,
        "report_path": report_path,
    }


# ── CLI Entry Point ───────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate trained salary models")
    parser.add_argument(
        "--config", default="ml/config.yaml", help="Path to config YAML"
    )
    args = parser.parse_args()

    result = run_evaluation(args.config)
    m = result["overall_metrics"]
    print("\n📊 Evaluation Results:")
    print(f"   MAE:  ${m['mae']:,.2f}")
    print(f"   RMSE: ${m['rmse']:,.2f}")
    print(f"   R2:   {m['r2']}")
    print(f"   MAPE: {m['mape']}%")

    for bias in result["bias_detection"]:
        flag = "FLAGGED" if bias.get("bias_flagged") else "OK"
        print(f"   Bias ({bias['group_column']}): {flag}")

    drift = result["drift_detection"]
    flag = "FLAGGED" if drift.get("drift_flagged") else "OK"
    print(f"   Drift: {flag}")
