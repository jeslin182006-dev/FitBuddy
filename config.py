import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'fitbuddy.db')}")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-flash")
GEMINI_TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash")
APP_NAME = "FitBuddy"
