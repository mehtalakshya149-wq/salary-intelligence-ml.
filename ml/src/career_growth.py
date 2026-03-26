"""
career_growth.py -- Career Growth Simulator
=============================================
Projects salary trajectory over 1, 3, and 5 years by
simulating experience-level promotions and role transitions.
Also recommends the next best role for maximum salary growth.
"""

import logging
from typing import Any

from ml.src.preprocess import load_config
from ml.src.predict import (
    load_model,
    load_encoders,
    preprocess_input,
    predict_salary,
    compute_confidence,
    adjust_for_inflation,
)

logger = logging.getLogger(__name__)


# -- Promotion Logic ----------------------------------------

# Years required at each level before promotion
PROMOTION_THRESHOLDS = {
    "en": 2,   # Entry -> Mid after 2 years
    "mi": 3,   # Mid -> Senior after 3 years
    "se": 5,   # Senior -> Executive after 5 years
    "ex": 99,  # Executive -- no auto-promotion
}

LEVEL_ORDER = ["en", "mi", "se", "ex"]


def _get_next_level(current_level: str) -> str:
    """Return the next experience level, or same if already max."""
    current = current_level.lower()
    idx = LEVEL_ORDER.index(current) if current in LEVEL_ORDER else 0
    next_idx = min(idx + 1, len(LEVEL_ORDER) - 1)
    return LEVEL_ORDER[next_idx]


def _apply_promotion_logic(
    profile: dict,
    years_ahead: int,
) -> list[dict]:
    """
    Simulate year-by-year promotions based on experience level.

    Logic:
    - Track cumulative years at current level
    - When years_at_level >= threshold, promote to next level
    - Each year also increments work_year

    Args:
        profile: Base profile dict.
        years_ahead: Number of years to simulate.

    Returns:
        List of profile snapshots, one per year.
    """
    snapshots = []
    current = profile.copy()
    current_level = str(current.get("experience_level", "en")).lower()
    years_at_level = 0
    base_year = int(current.get("work_year", 2026))

    for year_offset in range(1, years_ahead + 1):
        years_at_level += 1

        # Check for promotion
        threshold = PROMOTION_THRESHOLDS.get(current_level, 99)
        if years_at_level >= threshold:
            new_level = _get_next_level(current_level)
            if new_level != current_level:
                logger.info(
                    f"Year +{year_offset}: Promotion "
                    f"{current_level.upper()} -> {new_level.upper()}"
                )
                current_level = new_level
                years_at_level = 0

        snapshot = current.copy()
        snapshot["experience_level"] = current_level.upper()
        snapshot["work_year"] = base_year + year_offset
        snapshot["_year_offset"] = year_offset
        snapshot["_promoted_to"] = current_level.upper()
        snapshots.append(snapshot)

    return snapshots


# -- Growth Simulation --------------------------------------

def simulate_growth(
    profile: dict,
    years: list[int] | None = None,
    config_path: str = "ml/config.yaml",
) -> dict:
    """
    Predict salary at multiple future time points.

    For each target year, the profile is evolved with
    promotion logic and then passed through the prediction
    model.

    Args:
        profile: Current user profile dict.
        years: List of year offsets to predict (default: [1, 3, 5]).
        config_path: Path to config YAML.

    Returns:
        Dict with per-year predictions and growth metrics.
    """
    if years is None:
        years = [1, 3, 5]

    config = load_config(config_path)
    model_dir = config["paths"]["model_dir"]
    rf_model = load_model(model_dir, "random_forest")
    ensemble = load_model(model_dir, "ensemble")
    encoders = load_encoders(config)

    max_year = max(years)
    snapshots = _apply_promotion_logic(profile, max_year)

    # Predict current salary
    X_current = preprocess_input(profile.copy(), config, encoders)
    current_salary = predict_salary(rf_model, ensemble, X_current, config)
    current_confidence = compute_confidence(rf_model, X_current, config)

    # Predict at each target year
    projections = []
    for target_year in sorted(years):
        snapshot = snapshots[target_year - 1]  # 0-indexed

        X_future = preprocess_input(snapshot.copy(), config, encoders)
        future_salary = predict_salary(rf_model, ensemble, X_future, config)
        future_confidence = compute_confidence(rf_model, X_future, config)

        growth_pct = (
            (future_salary["average"] - current_salary["average"])
            / current_salary["average"] * 100
        ) if current_salary["average"] > 0 else 0.0

        projections.append({
            "year_offset": target_year,
            "experience_level": snapshot["_promoted_to"],
            "predicted_salary": future_salary,
            "confidence": future_confidence,
            "growth_from_current_pct": round(growth_pct, 2),
        })

    return {
        "current": {
            "salary": current_salary,
            "confidence": current_confidence,
            "experience_level": str(profile.get("experience_level", "EN")).upper(),
        },
        "projections": projections,
    }


# -- Role Recommendation -----------------------------------

# Macro role categories to test
ROLE_CANDIDATES = [
    "Data Scientist",
    "Data Engineer",
    "ML Engineer",
    "Data Analyst",
    "Analytics Engineer",
    "Data Architect",
    "MLOps Engineer",
    "Research Scientist",
]


def recommend_next_role(
    profile: dict,
    config_path: str = "ml/config.yaml",
    role_list: list[str] | None = None,
) -> list[dict]:
    """
    Predict salary across different job titles and recommend
    the top-3 highest-paying roles for the user's profile.

    The user's current profile is kept constant except for
    job_title, which is swapped for each candidate role.

    Args:
        profile: Current user profile dict.
        config_path: Path to config YAML.
        role_list: Roles to evaluate (default: ROLE_CANDIDATES).

    Returns:
        List of role recommendations sorted by salary descending.
    """
    config = load_config(config_path)
    model_dir = config["paths"]["model_dir"]
    rf_model = load_model(model_dir, "random_forest")
    ensemble = load_model(model_dir, "ensemble")
    encoders = load_encoders(config)

    roles = role_list or ROLE_CANDIDATES
    current_title = str(profile.get("job_title", "")).lower()

    # Predict current salary
    X_current = preprocess_input(profile.copy(), config, encoders)
    current_salary = predict_salary(rf_model, ensemble, X_current, config)

    recommendations = []
    for role in roles:
        variant = profile.copy()
        variant["job_title"] = role

        X_role = preprocess_input(variant, config, encoders)
        role_salary = predict_salary(rf_model, ensemble, X_role, config)

        delta = role_salary["average"] - current_salary["average"]
        delta_pct = (delta / current_salary["average"] * 100) if current_salary["average"] > 0 else 0.0

        recommendations.append({
            "role": role,
            "predicted_salary": role_salary,
            "salary_change": round(delta, 2),
            "change_pct": round(delta_pct, 2),
            "is_current": role.lower() == current_title,
        })

    # Sort by predicted salary descending
    recommendations.sort(key=lambda x: x["predicted_salary"]["average"], reverse=True)
    return recommendations


# -- Full Report --------------------------------------------

def get_growth_report(
    profile: dict,
    config_path: str = "ml/config.yaml",
) -> dict:
    """
    Complete career growth report combining:
    1. Multi-year salary trajectory (1, 3, 5 years)
    2. Top role recommendations

    Args:
        profile: Current user profile dict.
        config_path: Path to config YAML.

    Returns:
        Dict with trajectory and role recommendations.
    """
    trajectory = simulate_growth(profile, [1, 3, 5], config_path)
    role_recs = recommend_next_role(profile, config_path)

    # Top 3 roles (excluding current)
    top_roles = [r for r in role_recs if not r["is_current"]][:3]

    return {
        "trajectory": trajectory,
        "role_recommendations": role_recs,
        "top_3_new_roles": top_roles,
    }
