from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import re

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str

def generate_chat_response(user_message: str, history: List[dict] = None) -> str:
    """Core rule-based conversational logic."""
    msg = user_message.lower()
    
    # Career constraint enforcement: if it doesn't look like a career query and it's not a generic greeting
    greetings = ["hi", "hello", "hey", "help", "start"]
    if any(g in msg for g in greetings) and len(msg.split()) <= 3:
        return "👋 Hello! I'm your AI Career Assistant. I can help you with salary insights, skill recommendations, and career path advice. What would you like to know?"
    
    # Rule 1: Salary
    if "salary" in msg or "pay" in msg or "compensation" in msg:
        if "data scientist" in msg:
            return "Based on our latest intelligence, Data Scientists command an average salary of $125k to $145k depending on location and experience. Remote roles tend to have a slight premium for top-tier tech firms."
        elif "engineer" in msg or "ml" in msg or "machine learning" in msg:
            return "Machine Learning Engineers generally see starting salaries around $130k, scaling up past $160k with expertise in PyTorch, MLOps, and Kubernetes."
        elif "analyst" in msg:
            return "Data Analysts average between $75k to $95k. Adding advanced Python and Dashboarding skills (like Tableau) to your resume often drives salaries toward the upper band."
        else:
            return "Salaries can vary wildly by specific roles. Could you tell me exactly which tech or data role you're targeting so I can provide customized numbers?"
            
    # Rule 2: Skills
    elif "skill" in msg or "learn" in msg or "technolog" in msg or "tools" in msg:
        if "engineer" in msg:
            return "For Engineering roles, the highest ROI skills dynamically trending right now are Kubernetes, Cloud Architecture (AWS/GCP), and scalable system design."
        elif "data" in msg or "scientist" in msg or "analyst" in msg:
            return "Data roles heavily value deep expertise in Python, SQL, and advanced Machine Learning frameworks (like Scikit-Learn or PyTorch). If you're an analyst, definitely master SQL window functions!"
        else:
            return "The best skills depend on the role. Generally, Python and Cloud Computing show the highest cross-domain ROI on the market right now."
            
    # Rule 3: Career Advice / Growth
    elif "career" in msg or "promot" in msg or "advice" in msg or "growth" in msg or "path" in msg:
        return "To accelerate your career growth, consistently document your impact and dollar-value contributions to the company. Additionally, bridging the gap between technical execution and business strategy usually signals readiness for Senior or Lead promotions."
        
    # Rule 4: Match generic tech terms
    elif "python" in msg or "sql" in msg or "cloud" in msg:
        return "That's a fantastic area to focus on. Tools like Python, SQL, and Cloud platforms form the critical backbone of modern data infrastructure."
        
    # Constraint: Unknown / Out of scope
    else:
        return "Hmm... I specialize strictly in career progression, salary insights, and technical skill development. Could you rephrase your question to relate to your tech career?"

@router.post("/")
def chat_endpoint(request: ChatRequest):
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history] if request.history else []
    response_text = generate_chat_response(request.message, history_dicts)
    return ChatResponse(response=response_text)
