"""
DermaTwin AI — backend entrypoint.

Run with:
    uvicorn main:app --reload --port 8000

Requires backend/.env (copy from .env.example) with your real
YOUCAM_API_KEY / YOUCAM_SECRET_KEY. Without it, the app runs in mock
mode so the full pipeline is still demoable.
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from digital_twin import get_twin, update_twin
from agents import (
    skin_analysis_agent,
    beauty_scientist_agent,
    fashion_intelligence_agent,
    retail_concierge_agent,
    climate_agent,
    habit_coach_agent,
    shopping_intelligence_agent,
    audit_agent,
    prediction_agent,
    customer_assistant_agent,
)
from pydantic import BaseModel, Field

app = FastAPI(title="DermaTwin AI", version="0.1.0")


class AssistantRequest(BaseModel):
    user_id: str = Field(default="guest", min_length=1, max_length=120)
    question: str = Field(min_length=1, max_length=2000)
    use_twin: bool = False


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=120)
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=1000)
    topic: str = Field(default="assistant", max_length=80)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "DermaTwin AI backend running", "youcam_configured": bool(__import__('os').getenv("YOUCAM_API_KEY")), "assistant": "/assistant"}


@app.get("/health")
def health():
    return {"status": "ok", "youcam_configured": bool(__import__('os').getenv("YOUCAM_API_KEY"))}


@app.get("/twin/{user_id}")
def read_twin(user_id: str):
    return get_twin(user_id)


@app.post("/scan")
async def scan(
    user_id: str = Form(...),
    city: str = Form(None),
    allergies: str = Form(""),  # comma-separated
    selfie: UploadFile = File(...),
):
    """
    The core end-to-end pipeline:
    selfie -> skin analysis -> routine -> climate adjustment -> twin update
    """
    if selfie.content_type and not selfie.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="selfie must be an image")
    image_bytes = await selfie.read()
    if not image_bytes or len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="selfie must be between 1 byte and 10 MB")
    allergy_list = [a.strip() for a in allergies.split(",") if a.strip()]

    try:
        metrics = await skin_analysis_agent.analyze(image_bytes)
    except Exception as exc:
        from youcam_client import YouCamError

        if isinstance(exc, YouCamError):
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        raise
    routine = beauty_scientist_agent.build_routine(metrics, allergy_list)
    climate = await climate_agent.get_climate_context(city)
    routine = climate_agent.adjust_routine(routine, climate)
    colors = fashion_intelligence_agent.recommend_colors(metrics)

    twin = update_twin(
        user_id,
        skin_metrics=metrics,
        skincare_routine=routine,
        outfit_recommendations=colors,
        climate_context=climate,
    )

    streak = habit_coach_agent.get_streak(user_id)
    timeline = prediction_agent.project(metrics, streak, climate.get("uv_index"))
    twin = update_twin(user_id, predicted_timeline=timeline)

    audit_record = audit_agent.audit_scan(user_id, twin.model_dump())

    return {"twin": twin, "audit": audit_record}


@app.get("/predict/{user_id}")
def predict(user_id: str):
    """Re-run the prediction engine using the twin's latest stored metrics
    and current habit streak — lets the Mirror page refresh a projection
    after a habit check-in without requiring a new selfie scan."""
    twin = get_twin(user_id)
    if not twin.skin_metrics:
        return {"error": "Run /scan for this user first."}
    streak = habit_coach_agent.get_streak(user_id)
    uv = twin.climate_context.get("uv_index") if twin.climate_context else None
    timeline = prediction_agent.project(twin.skin_metrics, streak, uv)
    update_twin(user_id, predicted_timeline=timeline)
    return timeline


@app.get("/audit/{user_id}")
def audit_trail(user_id: str):
    return audit_agent.get_audit_trail(user_id)


@app.get("/audit")
def audit_trail_all():
    return audit_agent.get_audit_trail()


@app.get("/dashboard-summary")
def dashboard_summary():
    """Aggregate view for the retail/ops dashboard: all twins + audit stats."""
    from digital_twin import _TWINS  # local import keeps this endpoint's scope narrow

    twins = [t.model_dump() for t in _TWINS.values()]
    trail = audit_agent.get_audit_trail()
    anchored = sum(1 for r in trail if r["anchored_on_chain"])
    return {
        "total_users": len(twins),
        "total_scans": sum(1 for t in twins if t.get("skin_metrics")),
        "audit_events": len(trail),
        "onchain_anchored_events": anchored,
        "mock_anchored_events": len(trail) - anchored,
        "twins": twins,
        "recent_audit_events": trail[-20:],
    }


@app.post("/try-on")
async def try_on(garment_id: str = Form(...), selfie: UploadFile = File(...)):
    image_bytes = await selfie.read()
    return await fashion_intelligence_agent.try_on(image_bytes, garment_id)


@app.get("/deals/{user_id}")
def deals(user_id: str):
    twin = get_twin(user_id)
    return retail_concierge_agent.find_deals(twin.skincare_routine)


@app.post("/habit-checkin/{user_id}")
def checkin(user_id: str, routine_done: bool = Form(...), water_glasses: int = Form(0), sleep_hours: float = Form(0)):
    return habit_coach_agent.log_checkin(user_id, routine_done, water_glasses, sleep_hours)


@app.get("/shopping-prediction/{user_id}")
def shopping_prediction(user_id: str, tags: str = ""):
    twin = get_twin(user_id)
    if not twin.skin_metrics:
        return {"error": "Run /scan for this user first."}
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    return shopping_intelligence_agent.predict(twin.skin_metrics, tag_list)


@app.post("/assistant")
def assistant(request: AssistantRequest):
    twin = get_twin(request.user_id) if request.use_twin else None
    try:
        return customer_assistant_agent.answer(request.question, request.user_id, request.use_twin, twin)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/assistant/feedback")
def assistant_feedback(request: FeedbackRequest):
    try:
        return customer_assistant_agent.record_feedback(**request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/assistant/satisfaction")
def assistant_satisfaction():
    return customer_assistant_agent.satisfaction_summary()
