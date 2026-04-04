import google.generativeai as genai
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

def generate_ai_chat_response(user_message: str, history: List[dict] = None, api_key: str = None) -> str:
    """
    Handles conversational logic.
    Uses Google Gemini if API key is provided.
    Includes auto-discovery and quota-aware fallback (handles 404 and 429 errors).
    """
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # --- Dynamic Model Discovery ---
            available_models = []
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
            except Exception:
                available_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']
            
            if not available_models:
                return "⚠️ **AI Error:** No compatible models found for your API key."

            # Priority order: Flash is preferred for Free Tier because it has much higher quota limits
            priority = ['1.5-flash', '1.5-flash-latest', '1.5-pro', 'pro', '1.0-pro']
            
            # Reorder available models based on priority
            sorted_models = []
            for p in priority:
                for m in available_models:
                    if p in m.lower() and m not in sorted_models:
                        sorted_models.append(m)
            
            # Add any remaining models
            for m in available_models:
                if m not in sorted_models:
                    sorted_models.append(m)

            last_error = ""
            # --- Model Trial Loop ---
            for m_name in sorted_models:
                try:
                    model = genai.GenerativeModel(m_name)
                    
                    system_instruction = (
                        "You are an expert AI Career Advisor for the Salary Intelligence Platform. "
                        "Always remain professional and helpful. Focus on Data Science and AI careers."
                    )

                    transformed_history = []
                    if history:
                        for msg in history[:-1]:
                            role = "user" if msg['role'] == "user" else "model"
                            transformed_history.append({"role": role, "parts": [msg['content']]})

                    chat = model.start_chat(history=transformed_history)
                    response = chat.send_message(f"{system_instruction}\n\nUser: {user_message}")
                    return response.text
                    
                except Exception as e:
                    last_error = str(e)
                    # If 404 (Not Found) or 429 (Quota Exceeded), try the next model
                    if "404" in last_error or "429" in last_error or "quota" in last_error.lower():
                        continue
                    else:
                        return f"⚠️ **AI Error:** {last_error}"
            
            return f"⚠️ **AI Quota Error:** All available models are currently busy or out of free credits. Please wait 60 seconds and try again. ({last_error})"
            
        except Exception as e:
            return f"⚠️ **AI Error:** {str(e)}"

    # --- Mode 2: Rule-Based Fallback ---
    msg = user_message.lower()
    if "salary" in msg or "pay" in msg:
        return "In Basic Mode, I can tell you that Data Scientists generally earn $120k-$160k. Provide an API key for a deep-dive analysis!"
    return "I am currently in **Basic Mode**. Add a Gemini API key in the sidebar for full AI intelligence!"

@router.post("/")
def chat_endpoint(request: ChatRequest):
    history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history] if request.history else []
    response_text = generate_ai_chat_response(request.message, history_dicts, request.api_key)
    return ChatResponse(response=response_text)
