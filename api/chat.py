import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_ai_chat_response(user_message: str, history: list, api_key: str = None) -> str:
    key = api_key or os.getenv("XAI_API_KEY")

    if not key:
        return "⚠️ No API key found. Please enter your Groq API key in the sidebar or add XAI_API_KEY to your .env file."

    try:
        client = Groq(api_key=key)

        system_prompt = """You are an expert AI Career Advisor with deep knowledge of:
- Salary bands across industries, roles, and experience levels
- Career progression paths in tech, finance, healthcare, and more
- In-demand skills and their ROI in the job market
- Negotiation strategies for raises and promotions
- Resume and interview coaching

Be concise, data-driven, and actionable. When citing salaries, mention they are 
approximate and vary by location/company size. Format responses clearly."""

        messages = [{"role": "system", "content": system_prompt}]

        for msg in history[:-1]:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "authentication" in error_msg.lower():
            return "❌ Invalid API key. Please check your Groq API key in the sidebar."
        elif "429" in error_msg:
            return "⏳ Rate limit hit. Please wait a moment and try again."
        else:
            return f"⚠️ Something went wrong: {error_msg}"