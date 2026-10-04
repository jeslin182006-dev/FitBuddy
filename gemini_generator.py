from .config import GEMINI_WORKOUT_MODEL, GOOGLE_API_KEY


def _client():
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured. Add it to your .env file.")
    from google import genai
    return genai.Client(api_key=GOOGLE_API_KEY)


def _extract(response) -> str:
    text = getattr(response, "text", None)
    if text:
        return text.strip()
    return str(response).strip()


def generate_workout_gemini(username: str, age: int, weight: float, goal: str, intensity: str) -> str:
    client = _client()
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.
Create a safe, practical, personalized 7-day workout plan.

User:
- Name: {username}
- Age: {age}
- Weight: {weight} kg
- Goal: {goal}
- Preferred intensity: {intensity}

Return exactly these sections:
1. FITBUDDY SAFETY NOTE (brief; advise medical/professional guidance for pain, injury, or medical conditions)
2. 7-DAY WORKOUT PLAN
For Day 1 through Day 7 include:
- Focus
- Warm-up (5-10 minutes)
- Main workout with exercise, sets/reps or duration, and rest
- Cool-down/recovery
3. WEEKLY GUIDANCE

Do not diagnose medical conditions. Do not prescribe medication or extreme diets. Keep recommendations appropriate for a general wellness application.
"""
    response = client.models.generate_content(model=GEMINI_WORKOUT_MODEL, contents=prompt)
    return _extract(response)
