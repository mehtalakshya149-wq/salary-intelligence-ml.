"""
roadmaps.py — Learning Roadmap Generation Logic
==============================================
Maps skill gaps into a structured, time-bound curriculum.
"""

import logging

logger = logging.getLogger(__name__)

# --- Resource Knowledge Base ---
# Skill -> (Difficulty, Estimated Hours, Resource Name/Link)
SKILL_RESOURCES = {
    # Foundational
    "sql": ("Beginner", 20, "SQL for Data Science (Coursera)"),
    "excel": ("Beginner", 15, "Excel Skills for Business (Coursera)"),
    "tableau": ("Beginner", 25, "Data Visualization with Tableau (Udacity)"),
    "r": ("Beginner", 40, "Data Science: R Basics (edX)"),
    
    # Intermediate
    "python": ("Intermediate", 40, "Python for Data Science (IBM/edX)"),
    "aws": ("Intermediate", 30, "AWS Cloud Practitioner Essentials"),
    "gcp": ("Intermediate", 30, "Google Cloud Fundamentals"),
    "snowflake": ("Intermediate", 20, "Snowflake Hands-on Essentials"),
    "java": ("Intermediate", 50, "Java Programming Masterclass (Udemy)"),
    
    # Advanced / MLOps
    "tensorflow": ("Advanced", 60, "Deep Learning Specialization (DeepLearning.AI)"),
    "pytorch": ("Advanced", 60, "PyTorch for Deep Learning (Udemy)"),
    "docker": ("Advanced", 20, "Docker for Developers (FreeCodeCamp)"),
    "spark": ("Advanced", 40, "Spark and Python for Big Data (Udemy)"),
    "airflow": ("Advanced", 25, "Mastering Apache Airflow"),
    "kubernetes": ("Expert", 40, "Certified Kubernetes Administrator (CKA)"),
}

DEFAULT_RESOURCE = ("Intermediate", 30, "General Documentation & Hands-on Projects")

def generate_roadmap(missing_skills: list[str], weekly_hours: float = 10.0) -> dict:
    """
    Sequences skills into phases and calculates a realistic timeline.
    """
    phases = {
        "Foundational": [],
        "Professional": [],
        "Expert": []
    }
    
    total_hours = 0
    
    # Sort and sequence
    for skill in missing_skills:
        skill_clean = skill.lower().strip()
        diff, hours, resource = SKILL_RESOURCES.get(skill_clean, DEFAULT_RESOURCE)
        
        item = {
            "skill": skill.upper(),
            "difficulty": diff,
            "hours": hours,
            "resource": resource
        }
        
        if diff == "Beginner":
            phases["Foundational"].append(item)
        elif diff in ["Intermediate", "Advanced"]:
            phases["Professional"].append(item)
        else:
            phases["Expert"].append(item)
            
        total_hours += hours
        
    total_weeks = round(total_hours / weekly_hours, 1) if weekly_hours > 0 else 0
    
    # Flatten into chronological steps
    steps = phases["Foundational"] + phases["Professional"] + phases["Expert"]
    
    return {
        "phases": phases,
        "chronological_steps": steps,
        "total_estimated_hours": total_hours,
        "estimated_weeks": total_weeks,
        "weekly_pace": weekly_hours
    }
