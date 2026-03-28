"""
skill_gap.py — Skill Gap Analysis Engine
========================================
Compares user skillsets against market-derived requirements for
specific job titles to identify missing critical competencies.
"""

import logging
import pandas as pd
from ml.src.preprocess import load_config, load_data, clean_data

logger = logging.getLogger(__name__)

def get_market_requirements(job_title: str, config_path: str = "ml/config.yaml", top_n: int = 10) -> list[str]:
    """
    Extract the most frequent skills for a given job title from historical data.
    """
    try:
        config = load_config(config_path)
        df = clean_data(load_data(config["paths"]["raw_data"]), config)
        
        # Filter for similar titles (case-insensitive substring match)
        mask = df['job_title'].str.lower().str.contains(job_title.lower())
        subset = df[mask]
        
        if subset.empty:
            # Fallback to global top skills if no match
            subset = df
            
        all_skills = subset['skills'].str.split(',').explode().str.strip().str.lower()
        top_skills = all_skills.value_counts().head(top_n)
        
        return top_skills.index.tolist()
    except Exception as e:
        logger.error(f"Error extracting market requirements: {e}")
        return ["python", "sql", "machine learning", "aws", "docker"] # default fallback

def get_skill_gap_report(job_title: str, user_skills_str: str, config_path: str = "ml/config.yaml") -> dict:
    """
    Compares user skills against market requirements and generates a prioritized gap report.
    """
    market_skills = get_market_requirements(job_title, config_path)
    
    user_skills = [s.strip().lower() for s in user_skills_str.split(',') if s.strip()]
    user_skills_set = set(user_skills)
    
    missing_skills = [s for s in market_skills if s not in user_skills_set]
    matched_skills = [s for s in market_skills if s in user_skills_set]
    
    # Priority ranking based on frequency in market (market_skills is already sorted by freq)
    priority_ranking = missing_skills
    
    # Simple learning path logic
    path = []
    if missing_skills:
        foundational = [s for s in ["sql", "python", "excel", "tableau"] if s in missing_skills]
        advanced = [s for s in ["aws", "docker", "kubernetes", "tensorflow", "pytorch", "spark"] if s in missing_skills]
        
        if foundational:
            path.append(f"Phase 1 (Foundational): Master {', '.join(foundational[:2])}")
        if advanced:
            path.append(f"Phase 2 (Scalability): Learn {', '.join(advanced[:2])}")
        if len(missing_skills) > 4:
            path.append(f"Phase 3 (Niche/Expert): Focus on {', '.join(missing_skills[4:6])}")
    else:
        path.append("You already possess the top market/core skills for this role. Focus on portfolio differentiation.")

    return {
        "job_title": job_title,
        "market_top_skills": market_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "priority_ranking": priority_ranking,
        "learning_path": path,
        "match_percentage": round((len(matched_skills) / len(market_skills)) * 100, 1) if market_skills else 0
    }
