"""
skill_roi.py -- Skill ROI Calculator
======================================
Quantifies the salary impact of individual skills using
model perturbation: predict salary with and without each
skill, then compute the marginal uplift percentage.

This helps users understand which skills to invest in
for maximum salary return.
"""

import logging
from typing import Any

from ml.src.preprocess import load_config
from ml.src.predict import (
    load_model,
    load_encoders,
    preprocess_input,
    predict_salary,
)

logger = logging.getLogger(__name__)


# -- Skill Impact Computation -------------------------------

def compute_skill_impact(
    base_profile: dict,
    skill: str,
    rf_model: Any,
    ensemble_model: Any,
    encoders: dict,
    config: dict,
) -> dict:
    """
    Compute the marginal salary impact of adding a single skill.

    Method:
    1. Predict salary with the base profile (current skills)
    2. Add the target skill to the profile
    3. Predict salary again
    4. Compute delta = (new - base) / base * 100

    Args:
        base_profile: Dict of user features (must include 'skills').
        skill: Skill name to evaluate (e.g., 'TensorFlow').
        rf_model: Fitted RandomForestRegressor.
        ensemble_model: Fitted VotingRegressor.
        encoders: Dict with fitted encoder and scaler.
        config: Parsed config dict.

    Returns:
        Dict with skill name, base_salary, new_salary, and impact_pct.
    """
    # Baseline prediction (current skills)
    X_base = preprocess_input(base_profile.copy(), config, encoders)
    base_salary = predict_salary(rf_model, ensemble_model, X_base, config)

    # Augmented prediction (add the skill)
    augmented = base_profile.copy()
    current_skills = str(augmented.get("skills", ""))
    if skill.lower() not in current_skills.lower():
        augmented["skills"] = f"{current_skills}, {skill}" if current_skills else skill

    X_aug = preprocess_input(augmented, config, encoders)
    new_salary = predict_salary(rf_model, ensemble_model, X_aug, config)

    # Compute impact
    base_avg = base_salary["average"]
    new_avg = new_salary["average"]
    impact_pct = ((new_avg - base_avg) / base_avg * 100) if base_avg > 0 else 0.0

    return {
        "skill": skill,
        "base_salary": round(base_avg, 2),
        "new_salary": round(new_avg, 2),
        "salary_increase": round(new_avg - base_avg, 2),
        "impact_pct": round(impact_pct, 2),
    }


# -- Rank All Skills ----------------------------------------

def rank_skills(
    base_profile: dict,
    skill_list: list[str],
    rf_model: Any,
    ensemble_model: Any,
    encoders: dict,
    config: dict,
) -> list[dict]:
    """
    Rank a list of skills by their salary uplift for a given profile.

    Args:
        base_profile: Dict of user features.
        skill_list: List of skill names to evaluate.
        rf_model: Fitted RandomForestRegressor.
        ensemble_model: Fitted VotingRegressor.
        encoders: Dict with fitted encoder and scaler.
        config: Parsed config dict.

    Returns:
        List of dicts sorted by impact_pct descending.
    """
    results = []
    for skill in skill_list:
        impact = compute_skill_impact(
            base_profile, skill,
            rf_model, ensemble_model, encoders, config,
        )
        results.append(impact)
        logger.info(f"Skill '{skill}': {impact['impact_pct']:+.2f}%")

    # Sort by impact descending
    results.sort(key=lambda x: x["impact_pct"], reverse=True)
    return results


# -- Orchestrator -------------------------------------------

# Default skill pool for evaluation
DEFAULT_SKILLS = [
    "Python", "SQL", "R", "TensorFlow", "PyTorch", "Spark",
    "AWS", "GCP", "Docker", "Kubernetes", "Tableau", "Excel",
    "Scala", "Java", "Hadoop", "Airflow", "dbt", "Snowflake",
]


def get_roi_report(
    base_profile: dict,
    config_path: str = "ml/config.yaml",
    skill_list: list[str] | None = None,
) -> dict:
    """
    Generate a full Skill ROI report.

    Args:
        base_profile: User's current profile dict.
        config_path: Path to config YAML.
        skill_list: Skills to evaluate (defaults to DEFAULT_SKILLS).

    Returns:
        Dict with ranked skills and summary statistics.
    """
    config = load_config(config_path)
    model_dir = config["paths"]["model_dir"]

    rf_model = load_model(model_dir, "random_forest")
    ensemble = load_model(model_dir, "ensemble")
    encoders = load_encoders(config)

    skills = skill_list or DEFAULT_SKILLS

    # Filter out skills the user already has
    current_skills = str(base_profile.get("skills", "")).lower()
    new_skills = [s for s in skills if s.lower() not in current_skills]

    if not new_skills:
        return {
            "message": "You already have all evaluated skills.",
            "ranked_skills": [],
        }

    ranked = rank_skills(
        base_profile, new_skills,
        rf_model, ensemble, encoders, config,
    )

    # Summary
    positive = [r for r in ranked if r["impact_pct"] > 0]
    top_3 = ranked[:3] if len(ranked) >= 3 else ranked

    return {
        "ranked_skills": ranked,
        "top_3_skills": top_3,
        "total_evaluated": len(ranked),
        "positive_impact_count": len(positive),
        "best_skill": top_3[0]["skill"] if top_3 else None,
        "best_impact_pct": top_3[0]["impact_pct"] if top_3 else 0.0,
    }
