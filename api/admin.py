from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import User, SalaryPrediction, ModelLog
from api.auth import get_current_user
import sys
import os

router = APIRouter()

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Super-User privileges required.")
    return current_user

@router.get("/users")
def get_all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.query(User).all()
    return [{"id": str(u.id), "username": u.username, "email": u.email, "role": u.role, "created_at": u.created_at} for u in users]

@router.delete("/users/{username}")
def delete_user(username: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if username == admin.username:
        raise HTTPException(status_code=400, detail="Administrators cannot terminate their own instances.")
    u_del = db.query(User).filter(User.username == username).first()
    if not u_del:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(u_del)
    db.commit()
    return {"message": f"User {username} successfully deleted."}

@router.get("/predictions")
def get_global_predictions(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    preds = db.query(SalaryPrediction).order_by(SalaryPrediction.created_at.desc()).limit(50).all()
    return [{
        "username": p.user.username if p.user else "Unknown",
        "job_title": p.job_title,
        "experience": p.experience_level,
        "predicted_salary": p.predicted_average,
        "confidence": p.confidence_score,
        "created_at": p.created_at
    } for p in preds]

@router.get("/logs")
def get_system_logs(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    logs = db.query(ModelLog).order_by(ModelLog.timestamp.desc()).limit(100).all()
    return [{
        "username": l.user.username if l.user else "Unknown",
        "action": l.action,
        "endpoint": l.endpoint,
        "timestamp": l.timestamp
    } for l in logs]

def background_training_task():
    try:
        from ml.src.train import run_training
        run_training()
    except Exception as e:
        print(f"Background Training Failed: {e}")

@router.post("/retrain")
def trigger_retraining(background_tasks: BackgroundTasks, admin: User = Depends(require_admin)):
    """
    Triggers the global machine learning pipeline (ml.src.train) to rebuild 
    the Random Forest and Gradient Boosting ensemble using active database data.
    """
    background_tasks.add_task(background_training_task)
    return {"message": "Model retraining job offloaded to background worker successfully."}
