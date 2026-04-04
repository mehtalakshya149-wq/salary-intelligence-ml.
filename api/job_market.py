from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter()

MOCK_JOBS = [
    {"id": 1, "title": "Data Scientist", "company": "Tech Corp", "location": "Remote", "salary": 120000, "skills": ["Python", "SQL", "Machine Learning", "Pandas", "Scikit-Learn"]},
    {"id": 2, "title": "Data Scientist", "company": "Data Inc", "location": "New York", "salary": 125000, "skills": ["Python", "R", "SQL", "Tableau", "Statistics"]},
    {"id": 3, "title": "ML Engineer", "company": "AI startup", "location": "San Francisco", "salary": 140000, "skills": ["Python", "TensorFlow", "PyTorch", "AWS", "Docker"]},
    {"id": 4, "title": "ML Engineer", "company": "Big Tech", "location": "Seattle", "salary": 150000, "skills": ["Python", "C++", "PyTorch", "Kubernetes", "System Design"]},
    {"id": 5, "title": "Data Analyst", "company": "Finance LLC", "location": "Chicago", "salary": 90000, "skills": ["SQL", "Excel", "Tableau", "Python", "Dashboarding"]},
    {"id": 6, "title": "Data Analyst", "company": "Retail Co", "location": "Austin", "salary": 85000, "skills": ["SQL", "PowerBI", "Excel", "Communication"]},
    {"id": 7, "title": "Data Scientist", "company": "HealthCare AI", "location": "Boston", "salary": 130000, "skills": ["Python", "SQL", "NLP", "PyTorch", "AWS"]},
    {"id": 8, "title": "ML Engineer", "company": "Fintech Disrupt", "location": "Remote", "salary": 145000, "skills": ["Python", "Machine Learning", "Spark", "Kafka", "Cloud"]}
]

@router.get("/job-market-trends")
def get_job_market_trends():
    """Returns aggregated demand and average salary per role."""
    trends = {}
    for job in MOCK_JOBS:
        title = job["title"]
        if title not in trends:
            trends[title] = {"demand_count": 0, "total_salary": 0}
        trends[title]["demand_count"] += 1
        trends[title]["total_salary"] += job["salary"]
        
    result = []
    for title, data in trends.items():
        result.append({
            "role": title,
            "demand_count": data["demand_count"],
            "avg_salary": data["total_salary"] / data["demand_count"]
        })
    return {"trends": result}

@router.get("/top-skills-demand")
def get_top_skills_demand(role: Optional[str] = None):
    """Returns the most in-demand skills, optionally filtered by role."""
    skill_counts = {}
    for job in MOCK_JOBS:
        if role and job["title"].lower() != role.lower():
            continue
        for skill in job["skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
            
    # Sort skills by demand count (descending)
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
    return {"top_skills": [{"skill": k, "demand": v} for k, v in sorted_skills]}

@router.get("/job-recommendations")
def get_job_recommendations(user_skills: List[str] = Query(default=[])):
    """Recommends jobs based on skill matching, ranked by similarity score."""
    user_skills_set = {s.lower() for s in user_skills} if user_skills else set()
    
    recommendations = []
    for job in MOCK_JOBS:
        job_skills_set = {s.lower() for s in job["skills"]}
        
        if not job_skills_set:
            match_score = 0.0
        else:
            if user_skills_set:
                intersection = user_skills_set.intersection(job_skills_set)
                match_score = len(intersection) / len(job_skills_set)
            else:
                match_score = 0.0
            
        rec = job.copy()
        rec["match_score"] = round(match_score, 2)
        recommendations.append(rec)
        
    # Rank by match score descending, then by salary descending
    recommendations.sort(key=lambda x: (x["match_score"], x["salary"]), reverse=True)
    
    return {"recommendations": recommendations}
