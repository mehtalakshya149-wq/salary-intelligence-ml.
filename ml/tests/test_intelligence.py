"""
test_intelligence.py -- Smoke Tests for Intelligence Modules
==============================================================
Tests: Skill ROI, Career Growth, Salary Trends, Resume Parser
"""

import os
import sys
import logging

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ── Helpers ───────────────────────────────────────────────

SAMPLE_PROFILE = {
    "job_title": "Data Scientist",
    "experience_level": "MI",
    "employment_type": "FT",
    "company_location": "US",
    "company_size": "M",
    "remote_ratio": 50,
    "skills": "Python, SQL, TensorFlow",
    "work_year": 2025,
}

SAMPLE_RESUME = """
John Doe
Senior Data Scientist | 7+ years of experience

Skills: Python, SQL, TensorFlow, PyTorch, Spark, AWS, Docker,
scikit-learn, pandas, numpy, Tableau, Airflow

Experience:
- Senior Data Scientist at TechCorp (2022-Present)
  Led ML pipeline development for recommendation systems.
  8+ years in data science and machine learning.

- Data Scientist at StartupAI (2019-2022)
  Built predictive models for customer churn.

Education:
- M.S. Computer Science, Stanford University
- B.S. Statistics, UC Berkeley

Full-time position preferred.
"""


# ── Test Functions ────────────────────────────────────────

def test_skill_roi():
    """Test Skill ROI Calculator."""
    from ml.src.skill_roi import get_roi_report

    result = get_roi_report(SAMPLE_PROFILE.copy())

    assert "ranked_skills" in result, "Missing ranked_skills"
    assert len(result["ranked_skills"]) > 0, "No skills ranked"
    assert "impact_pct" in result["ranked_skills"][0], "Missing impact_pct"

    logger.info(
        f"PASS Skill ROI -- {result['total_evaluated']} skills evaluated, "
        f"best: {result['best_skill']} ({result['best_impact_pct']:+.2f}%)"
    )
    return result


def test_career_growth():
    """Test Career Growth Simulator."""
    from ml.src.career_growth import get_growth_report

    result = get_growth_report(SAMPLE_PROFILE.copy())

    assert "trajectory" in result, "Missing trajectory"
    projections = result["trajectory"]["projections"]
    assert len(projections) == 3, f"Expected 3 projections, got {len(projections)}"

    # Verify we have 1, 3, 5 year offsets
    offsets = [p["year_offset"] for p in projections]
    assert offsets == [1, 3, 5], f"Unexpected offsets: {offsets}"

    # Role recommendations should exist
    assert len(result["role_recommendations"]) > 0, "No role recommendations"

    current_sal = result["trajectory"]["current"]["salary"]["average"]
    yr5_sal = projections[2]["predicted_salary"]["average"]

    logger.info(
        f"PASS Career Growth -- "
        f"current: ${current_sal:,.0f}, 5yr: ${yr5_sal:,.0f}, "
        f"top role: {result['top_3_new_roles'][0]['role']}"
    )
    return result


def test_salary_trends():
    """Test Salary Trend Forecast."""
    from ml.src.salary_trends import get_trend_report

    result = get_trend_report(n_forecast_years=3)

    assert "yearly_stats" in result, "Missing yearly_stats"
    assert "trend" in result, "Missing trend"
    assert "forecast" in result, "Missing forecast"
    assert len(result["forecast"]) == 3, "Expected 3 forecast years"

    # Forecast years should be in the future
    last_hist_year = max(s["work_year"] for s in result["yearly_stats"])
    for fc in result["forecast"]:
        assert fc["year"] > last_hist_year, "Forecast year not in future"

    trend = result["trend"]
    logger.info(
        f"PASS Salary Trends -- "
        f"direction: {trend['direction']}, "
        f"slope: ${trend['slope']:,.0f}/yr, "
        f"R2: {trend['r_squared']}, "
        f"3yr forecast: ${result['forecast'][-1]['predicted_median']:,.0f}"
    )
    return result


def test_resume_parser():
    """Test Resume-to-Salary Estimation."""
    from ml.src.resume_parser import (
        extract_skills,
        extract_experience_level,
        extract_job_title,
        build_profile_from_resume,
        estimate_salary_from_resume,
        get_nlp_architecture_explanation,
    )

    # Unit tests for extractors
    skills = extract_skills(SAMPLE_RESUME)
    assert "python" in skills, "Should detect Python"
    assert "tensorflow" in skills, "Should detect TensorFlow"
    assert len(skills) >= 5, f"Expected 5+ skills, got {len(skills)}"

    level = extract_experience_level(SAMPLE_RESUME)
    assert level == "SE", f"Expected SE (senior), got {level}"

    title = extract_job_title(SAMPLE_RESUME)
    assert "Data Scientist" in title, f"Expected Data Scientist, got {title}"

    # Full estimation
    result = estimate_salary_from_resume(SAMPLE_RESUME)
    assert "salary_estimate" in result, "Missing salary_estimate"
    assert result["salary_estimate"]["average"] > 0, "Salary should be positive"

    # Architecture explanation
    arch = get_nlp_architecture_explanation()
    assert "current_approach" in arch, "Missing current_approach"
    assert len(arch["current_approach"]["stages"]) == 6, "Expected 6 stages"

    logger.info(
        f"PASS Resume Parser -- "
        f"{len(skills)} skills extracted, "
        f"level: {level}, title: {title}, "
        f"salary: ${result['salary_estimate']['average']:,.0f}"
    )
    return result


# ── Runner ────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Intelligence Modules -- Integration Tests")
    print("=" * 60)

    tests = [
        ("1/4: Skill ROI", test_skill_roi),
        ("2/4: Career Growth", test_career_growth),
        ("3/4: Salary Trends", test_salary_trends),
        ("4/4: Resume Parser", test_resume_parser),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        print(f"\n--- {name} ---\n")
        try:
            test_fn()
            passed += 1
        except Exception as e:
            logger.error(f"FAIL {name}: {e}")
            failed += 1
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"  Results: {passed}/{passed+failed} passed, {failed}/{passed+failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\nAll intelligence module tests passed!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
