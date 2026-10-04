from .config import GEMINI_TIP_MODEL, GOOGLE_API_KEY


def generate_nutrition_tip_with_flash(goal: str) -> str:
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured. Add it to your .env file.")
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY)
    prompt = f"""
You are FitBuddy. Give one concise, practical nutrition or recovery tip for a person whose fitness goal is: {goal}.
Keep it under 120 words. Prefer ordinary food, hydration, sleep, and recovery guidance.
Do not diagnose, prescribe supplements/medication, or recommend extreme calorie restriction.
"""
    response = client.models.generate_content(model=GEMINI_TIP_MODEL, contents=prompt)
    return (getattr(response, "text", None) or str(response)).strip()
