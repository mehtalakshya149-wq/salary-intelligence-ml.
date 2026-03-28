from fastapi import APIRouter, Depends
from ml.src.fairness import run_bias_audit
from api.deps import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def get_bias_report(current_user: dict = Depends(get_current_user)):
    """
    Generate and return a fairness & bias audit report.
    Analyzes historical datasets and prediction trends.
    """
    try:
        report = run_bias_audit("ml/config.yaml")
        return report
    except Exception as e:
        logger.error(f"Error generating bias report: {e}")
        return {"error": str(e)}
