"""
skill_roi.py -- Skill ROI Calculator
======================================
Quantifies the salary impact of individual skills using
model perturbation: we directly simulate what happens to
skills_count at different training-data levels, since the
OrdinalEncoder collapses all unseen skill strings to -1.

Skill tiers (mapped from training data range 2-6):
  Foundational  → skills_count target = 3
  Intermediate  → skills_count target = 4
  Advanced      → skills_count target = 5
  Expert        → skills_count target = 6
"""

import logging
from ml.src.preprocess import load_config
from ml.src.predict import (
    load_model,
    load_encoders,
    preprocess_input,
    predict_salary,
)

logger = logging.getLogger(__name__)


# ── Skill Tier Map ----------------------------------------

# Each skill is mapped to its expected skills_count target
# based on where similar profiles sit in the training data.
# Higher count = richer "expert stack" signal to the model.
SKILL_TIER_TARGET = {
    # Foundational (target skills_count = 3)
    "SQL": 3,
    "Excel": 3,
    "R": 3,
    "Tableau": 3,

    # Intermediate (target skills_count = 4)
    "Python": 4,
    "AWS": 4,
    "GCP": 4,
    "Java": 4,
    "Hadoop": 4,
    "Snowflake": 4,

    # Advanced (target skills_count = 5)
    "TensorFlow": 5,
    "PyTorch": 5,
    "Docker": 5,
    "Spark": 5,
    "Airflow": 5,
    "dbt": 5,
    "Scala": 5,

    # Expert / Architecture (target skills_count = 6)
    "Kubernetes": 6,
}

DEFAULT_TIER_TARGET = 4  # Fallback for unknown skills


# -- Skill Impact Computation -------------------------------

def compute_skill_impact(
    base_profile: dict,
    skill: str,
    rf_model,
    ensemble_model,
    encoders: dict,
    config: dict,
) -> dict:
    """
    Compute the salary impact of a skill using skills_count perturbation.

    The OrdinalEncoder encodes all unseen skill strings as -1, so we
    cannot distinguish profiles by the raw skills text at inference.
    Instead, we directly patch `skills_count` in the preprocessed matrix
    to the target level for this skill's tier (from SKILL_TIER_TARGET).

    Returns:
        Dict with skill name, base_salary, new_salary, impact_pct.
    """
    # Baseline prediction
    X_base = preprocess_input(base_profile.copy(), config, encoders)
    base_salary = predict_salary(rf_model, ensemble_model, X_base, config)

    # If user already has the skill, impact = 0
    current_skills = str(base_profile.get("skills", ""))
    if skill.lower() in current_skills.lower():
        return {
            "skill": skill,
            "base_salary": round(base_salary["average"], 2),
            "new_salary": round(base_salary["average"], 2),
            "salary_increase": 0.0,
            "impact_pct": 0.0,
        }

    # Current skills_count
    current_count = len([s for s in current_skills.split(",") if s.strip()])

    # Target skills_count for this skill's tier
    target_count = SKILL_TIER_TARGET.get(skill, DEFAULT_TIER_TARGET)

    # If user already has more skills than target, bump by 1
    if current_count >= target_count:
        target_count = current_count + 1

    # Patch skills_count in the preprocessed matrix
    X_aug = X_base.copy()
    if "skills_count" in X_aug.columns:
        X_aug["skills_count"] = float(target_count)

    new_salary = predict_salary(rf_model, ensemble_model, X_aug, config)

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
    rf_model,
    ensemble_model,
    encoders: dict,
    config: dict,
) -> list[dict]:
    """Rank a list of skills by their salary uplift for a given profile."""
    results = []
    for skill in skill_list:
        impact = compute_skill_impact(
            base_profile, skill,
            rf_model, ensemble_model, encoders, config,
        )
        results.append(impact)
        logger.info(f"Skill '{skill}': {impact['impact_pct']:+.2f}%")

    results.sort(key=lambda x: x["impact_pct"], reverse=True)
    return results


# -- Orchestrator -------------------------------------------

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
