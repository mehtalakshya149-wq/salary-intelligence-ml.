from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import User, SalaryPrediction

router = APIRouter()

def get_user_by_name(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/history")
def get_prediction_history(username: str, db: Session = Depends(get_db)):
    user = get_user_by_name(username, db)
    predictions = db.query(SalaryPrediction).filter(
        SalaryPrediction.user_id == user.id
    ).order_by(SalaryPrediction.created_at.desc()).all()
    
    return {"history": predictions}

@router.get("/analytics")
def get_analytics(username: str, db: Session = Depends(get_db)):
    user = get_user_by_name(username, db)
    predictions = db.query(SalaryPrediction).filter(
        SalaryPrediction.user_id == user.id
    ).order_by(SalaryPrediction.created_at.desc()).all()
    
    # 1. Salary Growth Graph (historical predictions)
    # We will format it as a list of dicts: time, salary
    growth_data = []
    if predictions:
        growth_data = [
            {"date": p.created_at.strftime("%Y-%m-%d %H:%M"), "predicted_salary": p.predicted_average}
            for p in reversed(predictions[:15])  # Reverse to get chronological order for the chart
        ]
    
    # 2. Market Value Score (pseudo-metric)
    market_value_score = 0.0
    if predictions:
        latest = predictions[0]
        # Dynamic base score + confidence score impact
        market_value_score = min(100.0, 60.0 + (latest.confidence_score * 40.0))
    
    # 3. Skill Recommendations
    recommendations = []
    if predictions:
        latest_job = predictions[0].job_title.lower()
        if "scientist" in latest_job:
            recommendations = ["Deep Learning", "MLOps", "Cloud Architecture"]
        elif "engineer" in latest_job:
            recommendations = ["System Design", "Rust", "Kubernetes", "Kafka"]
        elif "analyst" in latest_job:
            recommendations = ["Advanced SQL", "Data Engineering", "Python", "Tableau"]
        else:
            recommendations = ["Python", "Cloud Computing", "Leadership", "Agile"]
    else:
        recommendations = ["Python", "SQL", "Communication"]
            
    return {
        "market_value_score": round(market_value_score, 1),
        "salary_growth": growth_data,
        "recommendations": recommendations,
        "total_predictions": len(predictions)
    }
