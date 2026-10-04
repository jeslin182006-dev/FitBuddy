# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite web application that uses Google Gemini to generate personalized 7-day workout plans, nutrition/recovery tips, and feedback-based plan revisions.

## Features

- Personalized 7-day workout plan
- Goal/intensity-based generation
- Nutrition/recovery tip
- Feedback-based plan regeneration
- SQLite + SQLAlchemy persistence
- Admin/coach dashboard
- Delete user and associated plans
- FastAPI Swagger docs at `/docs`
- Configurable Gemini model names via `.env`

## Project structure

```text
fitbuddy/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── style.css
├── templates/
│   ├── all_users.html
│   ├── base.html
│   ├── feedback.html
│   ├── index.html
│   └── result.html
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Windows / VS Code setup

1. Install Python 3.11+.
2. Open this `fitbuddy` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv venv
```

5. Activate it:

```powershell
venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Create `.env` by copying `.env.example`.
8. Put your Gemini API key in `.env`:

```env
GOOGLE_API_KEY=your_real_key_here
```

9. Start the server:

```powershell
uvicorn app.main:app --reload
```

10. Open:

- Website: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Admin dashboard: http://127.0.0.1:8000/view-all-users

## Test flow

### Test 1 – Generate a plan

Use sample values:
- Name: Arun
- User ID: FB001
- Age: 22
- Weight: 68
- Goal: muscle gain
- Intensity: medium

Click **Generate My 7-Day Plan**.

### Test 2 – Update the plan

Open **Update Plan** and use:
- User ID: FB001
- Feedback: `Add more cardio and make Day 3 a recovery day.`

Submit and verify the revised 7-day plan.

### Test 3 – Dashboard

Open `/view-all-users` and verify the user, original plan, updated plan, and feedback.

### Test 4 – API documentation

Open `/docs` to inspect the FastAPI application. The primary user-facing workflow is HTML form based; `/docs` is useful for exploring the application routes and generated OpenAPI schema.

## Important

Never commit `.env` or your API key to GitHub. The application is intended for general wellness support, not medical diagnosis or treatment.
