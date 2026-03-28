from fastapi import APIRouter, Depends, Query
from ml.src.interview_data import get_suggested_questions
from api.deps import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def get_interview_questions(
    role: str = Query("Data Scientist"),
    difficulty: str = Query("Medium"),
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch curated interview questions based on role and difficulty.
    """
    try:
        questions = get_suggested_questions(role, difficulty)
        return {"role": role, "difficulty": difficulty, "questions": questions}
    except Exception as e:
        logger.error(f"Error fetching questions: {e}")
        return {"error": str(e)}
