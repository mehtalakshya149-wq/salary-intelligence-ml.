from fastapi import APIRouter, Depends, Body
from ml.src.resume_service import analyze_resume_text, get_company_recommendations
from api.deps import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def analyze_resume(
    payload: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze resume text and provide job recommendations.
    """
    try:
        text = payload.get("text", "")
        target_role = payload.get("target_role")
        
        if not text:
            return {"error": "No resume text provided."}
            
        analysis = analyze_resume_text(text, target_role)
        
        # Add company recommendations based on best role
        best_role = analysis["target_analysis"]["role"]
        analysis["companies"] = get_company_recommendations(best_role)
        
        return analysis
    except Exception as e:
        logger.error(f"Resume analysis failed: {e}")
        return {"error": str(e)}
