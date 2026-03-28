"""
resume_service.py — Resume Parsing & Matching Engine
===================================================
Extracts skills from text and matches them against role requirements.
"""

import re
import pandas as pd
import numpy as np
from ml.src.preprocess import load_config, load_data, clean_data

# Common Data Science / Tech Skills for extraction
SKILL_DB = {
    "Programming": ["python", "sql", "r", "java", "scala", "c++", "javascript", "julia"],
    "Data Science": ["machine learning", "deep learning", "nlp", "computer vision", "statistics", "statistical analysis", "data mining", "predictive modeling"],
    "Frameworks": ["scikit-learn", "tensorflow", "pytorch", "keras", "pandas", "numpy", "matplotlib", "seaborn", "spark", "hadoop"],
    "Visualization": ["tableau", "power bi", "d3.js", "plotly", "looker"],
    "Cloud/DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "git", "jenkins", "airflow", "snowflake"],
    "Roles": ["data scientist", "data analyst", "data engineer", "ml engineer", "machine learning engineer", "research scientist"]
}

ROLE_REQUIREMENTS = {
    "Data Scientist": ["python", "sql", "machine learning", "statistics", "pandas", "scikit-learn"],
    "Data Analyst": ["sql", "excel", "tableau", "power bi", "statistics", "python"],
    "Data Engineer": ["sql", "python", "spark", "hadoop", "aws", "docker", "airflow"],
    "ML Engineer": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "docker"]
}

def extract_skills(text: str) -> list:
    """
    Simple keyword-based skill extraction from raw text.
    """
    found_skills = []
    text_lower = text.lower()
    
    for category, skills in SKILL_DB.items():
        for skill in skills:
            # Use regex for better matching (word boundaries)
            if re.search(rf"\b{re.escape(skill)}\b", text_lower):
                found_skills.append(skill)
                
    return sorted(list(set(found_skills)))

def analyze_resume_text(text: str, target_role: str = None) -> dict:
    """
    Full analysis pipeline: Parsing -> Matching -> Scoring.
    """
    extracted_skills = extract_skills(text)
    
    # If no target role provided, find the best match
    matches = {}
    for role, reqs in ROLE_REQUIREMENTS.items():
        # Skill match score (0-100)
        intersection = set(extracted_skills).intersection(set(reqs))
        base_match = (len(intersection) / len(reqs)) * 100
        
        # Add bonus for role-specific keywords in the text
        role_keywords = [role.lower()]
        if role == "ML Engineer":
            role_keywords.append("machine learning engineer")
            
        role_bonus = 0
        for kw in role_keywords:
            if kw in text.lower():
                role_bonus += 5 # Small boost for explicit role mention
                
        matches[role] = round(base_match + role_bonus, 1)
        
    # Tie-breaking logic
    # 1. Sort by score (desc)
    # 2. If scores are close, prefer target_role if it exists
    sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    best_role, best_score = sorted_matches[0]
    
    if target_role and target_role in matches:
        # If target role is within 10% of the best score, use it as best_role
        if matches[target_role] >= (best_score - 10):
            best_role = target_role
            best_score = matches[target_role]

    current_role = best_role
        
    # Selection Probability (Dummy logic based on skill match + length of text as exp proxy)
    skill_score = base_match # Use base match for probability calculation
    exp_factor = min(1.0, len(text.split()) / 500) # Assumes 500 words is 'vibrant' experience
    probability = round((skill_score * 0.7) + (exp_factor * 30), 1)
    
    # Skill Gaps
    target_reqs = ROLE_REQUIREMENTS.get(current_role, [])
    missing = [s for s in target_reqs if s not in extracted_skills]
    
    # Improvement Tips
    tips = []
    if len(extracted_skills) < 5:
        tips.append("Add more specific technical keywords to your resume.")
    if "python" not in extracted_skills and "sql" not in extracted_skills:
        tips.append("Focus on core data languages: Python and SQL are mandatory for most roles.")
    if len(text.split()) < 200:
        tips.append("Your resume seems too brief. Expand on your project impacts and responsibilities.")
    if not missing:
        tips.append("Your skill match is excellent! Focus on quantifying your achievements next.")
    else:
        tips.append(f"To reach 100% match for {current_role}, add: {', '.join(missing[:3])}")

    return {
        "extracted_skills": extracted_skills,
        "recommendations": sorted(matches.items(), key=lambda x: x[1], reverse=True),
        "target_analysis": {
            "role": current_role,
            "match_score": skill_score,
            "probability_score": probability,
            "missing_skills": missing
        },
        "tips": tips
    }

def get_company_recommendations(role: str, config_path: str = "ml/config.yaml") -> list:
    """
    Suggest companies from the dataset that hire for the recommended role.
    """
    try:
        config = load_config(config_path)
        df_raw = load_data(config["paths"]["raw_data"])
        # Filter by job title (loose match)
        role_df = df_raw[df_raw["job_title"].str.contains(role, case=False, na=False)]
        
        # In this dataset, we don't have company names, but we have company_size and location.
        # We will mock 'Company Names' based on size for UX diversity.
        names = {
            "L": ["Enterprise Partners", "Global Solutions", "Major Tech Inc"],
            "M": ["Midstack Analytics", "Growing Data Corp", "NextGen Systems"],
            "S": ["Startup Sphere", "Agile Insights", "Innovate AI"]
        }
        
        # Get most common size for this role
        if not role_df.empty:
            best_size = role_df["company_size"].mode()[0]
            return names.get(best_size, names["M"])
        return names["M"]
        
    except Exception:
        return ["Major Tech Inc", "Data Dynamics", "AI Ventures"]
