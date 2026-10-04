import os
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import (
    init_db,
    delete_user,
    get_all_users_with_plans,
    get_latest_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)
router = APIRouter()
init_db()


def page_context(request: Request, **kwargs):
    return {"request": request, **kwargs}


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", page_context(request))


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        data = UserInput(
            username=username.strip(), user_id=user_id.strip(), age=age,
            weight=weight, goal=goal.strip(), intensity=intensity.lower()
        )
        workout_plan = generate_workout_gemini(**data.model_dump())
        nutrition_tip = generate_nutrition_tip_with_flash(data.goal)
        save_user(data.model_dump())
        save_plan(data.user_id, workout_plan, nutrition_tip)
        return templates.TemplateResponse(
            "result.html",
            page_context(request, username=data.username, user_id=data.user_id,
                         age=data.age, weight=data.weight, goal=data.goal,
                         intensity=data.intensity, workout_plan=workout_plan,
                         nutrition_tip=nutrition_tip, message=None)
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html", page_context(request, error=f"Could not generate plan: {exc}"), status_code=500
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    try:
        user = get_user(user_id.strip())
        plan = get_latest_plan(user_id.strip())
        if not user or not plan:
            return templates.TemplateResponse("feedback.html", page_context(request, error="User ID not found."), status_code=404)
        payload = FeedbackRequest(user_id=user_id.strip(), feedback=feedback.strip())
        revised = update_workout_plan(plan.original_plan, payload.feedback, user.goal, user.intensity)
        updated = update_plan(payload.user_id, revised, payload.feedback)
        return templates.TemplateResponse(
            "result.html",
            page_context(request, username=user.username, user_id=user.user_id,
                         age=user.age, weight=user.weight, goal=user.goal,
                         intensity=user.intensity,
                         workout_plan=updated.updated_plan if updated else revised,
                         nutrition_tip=plan.nutrition_tip,
                         message="Your workout plan has been updated using your feedback.")
        )
    except Exception as exc:
        return templates.TemplateResponse("feedback.html", page_context(request, error=f"Could not update plan: {exc}"), status_code=500)


@router.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request):
    return templates.TemplateResponse("feedback.html", page_context(request))


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    records = get_all_users_with_plans()
    return templates.TemplateResponse("all_users.html", page_context(request, records=records))


@router.post("/delete-user/{user_id}")
def remove_user(user_id: str):
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)
