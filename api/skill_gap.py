from fastapi import APIRouter, Depends, Body
from ml.src.skill_gap import get_skill_gap_report
from api.deps import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def analyze_skill_gap(
    job_title: str = Body(..., embed=True),
    skills: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user)
):
    """
    Perform a skill gap analysis comparing user skills with market requirements.
    """
    try:
        report = get_skill_gap_report(job_title, skills, "ml/config.yaml")
        return report
    except Exception as e:
        logger.error(f"Error analyzing skill gap: {e}")
        return {"error": str(e)}
