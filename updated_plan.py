from .config import GEMINI_WORKOUT_MODEL, GOOGLE_API_KEY


def update_workout_plan(original_plan: str, feedback: str, goal: str, intensity: str) -> str:
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not configured. Add it to your .env file.")
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY)
    prompt = f"""
You are FitBuddy. Revise the existing 7-day workout plan using the user's feedback.

Fitness goal: {goal}
Intensity: {intensity}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Return a complete revised 7-day plan, not just a list of changes. Preserve useful parts while applying the feedback.
For every day include focus, warm-up, exercises with sets/reps or duration/rest, and cool-down/recovery.
Add a short safety note. Do not diagnose medical conditions or prescribe medication/extreme diets.
"""
    response = client.models.generate_content(model=GEMINI_WORKOUT_MODEL, contents=prompt)
    return (getattr(response, "text", None) or str(response)).strip()
