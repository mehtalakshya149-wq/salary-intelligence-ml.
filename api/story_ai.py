from fastapi import APIRouter, Depends, Body
from ml.src.story_ai import generate_story
from api.deps import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def get_explain_story(
    inputs: dict = Body(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Generate a human-readable story explaining a model prediction.
    """
    try:
        story = generate_story(inputs, "ml/config.yaml")
        return story
    except Exception as e:
        logger.error(f"Error generating explain story: {e}")
        return {"error": str(e)}
