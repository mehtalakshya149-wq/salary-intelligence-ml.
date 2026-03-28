from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import random

from api.database import get_db
from api.models import Notification, SalaryPrediction

router = APIRouter()

class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class GenerateRequest(BaseModel):
    user_id: str

@router.get("/", response_model=List[NotificationResponse])
def get_user_notifications(user_id: str, db: Session = Depends(get_db)):
    """Fetch all chronologically sorted notifications for a given user."""
    notifications = db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()
    # Map Integer to bool for Pydantic response
    for n in notifications:
        n.is_read = bool(n.is_read)
    return notifications

@router.post("/generate-notifications", response_model=dict)
def generate_opportunities(payload: GenerateRequest, db: Session = Depends(get_db)):
    """
    Simulates checking background AI pipelines to detect:
    1. Skill demand increases
    2. Salary growth opportunities
    """
    user_id = payload.user_id
    
    # Check what the user has predicted recently to tailor the alert
    latest_pred = db.query(SalaryPrediction).filter(SalaryPrediction.user_id == user_id).order_by(SalaryPrediction.created_at.desc()).first()
    
    skill_alerts = [
        ("Skill Demand Surge: PyTorch", "We tracked a 14% increase in job postings requiring PyTorch in the last 30 days. Consider updating your portfolio!"),
        ("Skill Demand Surge: MLOps", "Companies are prioritizing deployment architectures. Adding AWS/Docker to your profile can boost your compensation by 8%."),
        ("Skill Demand Surge: Generative AI", "LLM integrations are trending heavily in your sector. Familiarity with LangChain is now a top-tier asset.")
    ]
    
    salary_alerts = [
        ("Salary Growth Opportunity", "Market medians have adjusted upward for Senior-level roles in your area by 6%. Prepare your negotiation metrics."),
        ("Remote Premium Identified", "100% Remote roles for your title are currently out-earning hybrid roles. Filter your search criteria to maximize ROI."),
        ("Sector Expansion", "FinTech companies are actively recruiting profiles similar to yours with compensation bands 12% above market average.")
    ]
    
    # Generate 1 or 2 new notifications
    num_to_generate = random.choice([1, 2])
    generated_count = 0
    
    # Always include a salary one
    sal_title, sal_msg = random.choice(salary_alerts)
    if latest_pred:
        sal_msg = f"For trailing '{latest_pred.job_title}' roles: " + sal_msg
        
    db.add(Notification(user_id=user_id, title=sal_title, message=sal_msg))
    generated_count += 1
    
    if num_to_generate == 2:
        sk_title, sk_msg = random.choice(skill_alerts)
        db.add(Notification(user_id=user_id, title=sk_title, message=sk_msg))
        generated_count += 1
        
    db.commit()
    
    return {"message": f"Successfully generated {generated_count} new notifications."}

@router.put("/{notification_id}/read", response_model=dict)
def mark_read(notification_id: str, db: Session = Depends(get_db)):
    """Marks a notification as read."""
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notif.is_read = 1
    db.commit()
    return {"message": "Notification updated."}
