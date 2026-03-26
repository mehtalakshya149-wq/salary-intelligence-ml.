"""
smoke_test.py — End-to-End ML Pipeline Smoke Test
===================================================
Generates a synthetic salary dataset and runs every pipeline
stage to verify correctness. No real data required.

Usage:
    cd ghost-eclipse
    python -m ml.tests.smoke_test
"""

import os
import sys
import json
import shutil
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# ── Synthetic Data Generation ─────────────────────────────

def generate_synthetic_data(n_rows: int = 300) -> pd.DataFrame:
    """
    Create a realistic synthetic salary dataset for testing.
    """
    np.random.seed(42)

    job_titles = [
        "Data Scientist", "Data Engineer", "ML Engineer",
        "Data Analyst", "Analytics Engineer", "Research Scientist",
        "Data Architect", "BI Analyst", "NLP Engineer",
        "MLOps Engineer", "Business Analyst", "Head of Data",
    ]
    experience_levels = ["EN", "MI", "SE", "EX"]
    employment_types = ["FT", "PT", "CT", "FL"]
    locations = ["US", "GB", "DE", "CA", "IN", "FR", "AU", "BR", "NL", "ES"]
    company_sizes = ["S", "M", "L"]
    skill_pool = [
        "Python", "SQL", "R", "TensorFlow", "PyTorch", "Spark",
        "AWS", "GCP", "Docker", "Kubernetes", "Tableau", "Excel",
    ]

    # Base salary by experience
    exp_salary = {"EN": 55000, "MI": 85000, "SE": 130000, "EX": 190000}

    rows = []
    for _ in range(n_rows):
        exp = np.random.choice(experience_levels, p=[0.2, 0.3, 0.35, 0.15])
        emp = np.random.choice(employment_types, p=[0.75, 0.1, 0.1, 0.05])
        loc = np.random.choice(locations)
        size = np.random.choice(company_sizes, p=[0.25, 0.5, 0.25])
        remote = np.random.choice([0, 50, 100], p=[0.3, 0.3, 0.4])
        year = np.random.choice([2020, 2021, 2022, 2023, 2024, 2025])
        n_skills = np.random.randint(2, 7)
        skills = ", ".join(np.random.choice(skill_pool, n_skills, replace=False))

        # Generate salary with realistic variance
        base = exp_salary[exp]
        location_mult = 1.3 if loc in ["US", "CH", "AU"] else 1.0
        size_mult = {"S": 0.85, "M": 1.0, "L": 1.15}[size]
        remote_bonus = 1.05 if remote == 100 else 1.0
        noise = np.random.normal(1.0, 0.12)
        salary = base * location_mult * size_mult * remote_bonus * noise

        rows.append({
            "job_title": np.random.choice(job_titles),
            "experience_level": exp,
            "employment_type": emp,
            "company_location": loc,
            "company_size": size,
            "remote_ratio": remote,
            "skills": skills,
            "work_year": year,
            "salary_in_usd": round(max(salary, 15000), 2),
        })

    return pd.DataFrame(rows)


# ── Tests ─────────────────────────────────────────────────

def test_preprocess(config_path: str):
    """Test data loading, validation, cleaning, and encoding."""
    from ml.src.preprocess import build_pipeline

    X, y, config = build_pipeline(config_path)

    assert X.shape[0] > 0, "X has no rows"
    assert y.shape[0] > 0, "y has no rows"
    assert X.shape[0] == y.shape[0], "X and y row count mismatch"
    assert X.isnull().sum().sum() == 0, "X contains null values"
    assert y.isnull().sum() == 0, "y contains null values"

    logger.info(f"PASS Preprocess -- X: {X.shape}, y: {y.shape}")
    return X, y, config


def test_feature_engineering(X: pd.DataFrame, config: dict):
    """Test feature engineering creates expected columns."""
    from ml.src.feature_engineering import engineer_features

    X_eng = engineer_features(X.copy(), config)

    expected_features = ["experience_bin", "is_remote", "company_tier"]
    for feat in expected_features:
        assert feat in X_eng.columns, f"Missing feature: {feat}"

    assert len(X_eng.columns) > len(X.columns), "No features were added"

    logger.info(f"PASS Feature engineering -- {len(X_eng.columns)} columns")
    return X_eng


def test_training(config_path: str):
    """Test full training pipeline."""
    from ml.src.train import run_training

    result = run_training(config_path)

    model_dir = result["model_dir"]
    assert os.path.exists(os.path.join(model_dir, "ensemble.joblib"))
    assert os.path.exists(os.path.join(model_dir, "random_forest.joblib"))
    assert os.path.exists(os.path.join(model_dir, "gradient_boosting.joblib"))
    assert result["metadata"]["cross_validation"]["cv_r2_mean"] > -1.0

    logger.info(
        f"PASS Training -- CV R2: "
        f"{result['metadata']['cross_validation']['cv_r2_mean']}"
    )
    return result


def test_evaluation(config_path: str):
    """Test evaluation pipeline with bias/drift detection."""
    from ml.src.evaluate import run_evaluation

    result = run_evaluation(config_path)

    assert result["overall_metrics"]["r2"] > -1.0, "R2 is unreasonably low"
    assert result["overall_metrics"]["mae"] >= 0, "MAE cannot be negative"
    assert os.path.exists(result["report_path"])

    logger.info(
        f"PASS Evaluation -- R2: {result['overall_metrics']['r2']}, "
        f"MAE: ${result['overall_metrics']['mae']:,.2f}"
    )
    return result


def test_prediction(config_path: str):
    """Test single-instance prediction with confidence and inflation."""
    from ml.src.predict import run_prediction

    sample_input = {
        "job_title": "Data Scientist",
        "experience_level": "SE",
        "employment_type": "FT",
        "company_location": "US",
        "company_size": "L",
        "remote_ratio": 100,
        "skills": "Python, SQL, TensorFlow",
        "work_year": 2023,
    }

    result = run_prediction(sample_input, config_path)

    assert "salary" in result
    assert result["salary"]["min"] <= result["salary"]["average"] <= result["salary"]["max"]
    assert 0 <= result["confidence"]["score"] <= 100
    assert result["inflation_adjusted"]["multiplier"] >= 1.0

    logger.info(
        f"PASS Prediction -- avg: ${result['salary']['average']:,.2f}, "
        f"confidence: {result['confidence']['score']}% ({result['confidence']['label']})"
    )
    return result


def test_explainability(config_path: str):
    """Test SHAP global explanations."""
    from ml.src.explainability import run_explainability

    result = run_explainability(config_path)

    assert len(result["feature_importance"]) > 0, "No feature importances"
    assert os.path.exists(result["plots"]["summary"])
    assert os.path.exists(result["plots"]["bar"])

    top_feature = list(result["feature_importance"].keys())[0]
    logger.info(f"PASS Explainability -- top feature: {top_feature}")
    return result


# ── Main ──────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Salary Intelligence Platform -- ML Pipeline Smoke Test")
    print("=" * 60)

    # Setup: generate synthetic data
    config_path = "ml/config.yaml"
    raw_dir = "ml/data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    raw_path = os.path.join(raw_dir, "salaries.csv")

    df = generate_synthetic_data(300)
    df.to_csv(raw_path, index=False, encoding="utf-8")
    logger.info(f"Generated {len(df)} synthetic rows -> {raw_path}")

    # Run all tests
    passed = 0
    failed = 0
    total = 6

    try:
        print("\n--- 1/6: Preprocessing ---")
        X, y, config = test_preprocess(config_path)
        passed += 1
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"[X] Preprocess failed: {e}")
        failed += 1
        return

    try:
        print("\n--- 2/6: Feature Engineering ---")
        test_feature_engineering(X, config)
        passed += 1
    except Exception as e:
        logger.error(f"[X] Feature engineering failed: {e}")
        failed += 1

    try:
        print("\n--- 3/6: Training ---")
        test_training(config_path)
        passed += 1
    except Exception as e:
        logger.error(f"[X] Training failed: {e}")
        failed += 1
        return

    try:
        print("\n--- 4/6: Evaluation ---")
        test_evaluation(config_path)
        passed += 1
    except Exception as e:
        logger.error(f"[X] Evaluation failed: {e}")
        failed += 1

    try:
        print("\n--- 5/6: Prediction ---")
        test_prediction(config_path)
        passed += 1
    except Exception as e:
        logger.error(f"[X] Prediction failed: {e}")
        failed += 1

    try:
        print("\n--- 6/6: Explainability ---")
        test_explainability(config_path)
        passed += 1
    except Exception as e:
        logger.error(f"[X] Explainability failed: {e}")
        failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"  Results: {passed}/{total} passed, {failed}/{total} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    else:
        print("\n[*] All smoke tests passed!")


if __name__ == "__main__":
    main()
