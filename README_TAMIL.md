# FitBuddy – Simple Tamil Setup

1. VS Code-la `fitbuddy` folder open pannunga.
2. Terminal open pannunga.
3. Run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

4. `.env.example` copy panni `.env` create pannunga.
5. `.env`-la Gemini API key podunga:

```env
GOOGLE_API_KEY=YOUR_KEY
```

6. Server run:

```powershell
uvicorn app.main:app --reload
```

7. Browser-la `http://127.0.0.1:8000` open pannunga.

8. Sample:
- Name: Arun
- User ID: FB001
- Age: 22
- Weight: 68
- Goal: muscle gain
- Intensity: medium

9. Plan generate pannunga.
10. Update Plan page-la same User ID + feedback kuduthu revised plan test pannunga.
11. Dashboard: `http://127.0.0.1:8000/view-all-users`

**API key-ai GitHub-ku upload panna koodathu.** `.env` `.gitignore`-la already included.
