"""Agent 9 — Prediction Engine (powers the Skin Aging Simulator / AI Mirror).

Projects skin metrics forward in time. The direction of travel for each
horizon depends on two signals already in the twin:
  - habit adherence (from the Habit Coach's streak) — consistent routine
    use nudges "bad" metrics down and hydration up
  - climate exposure (UV/pollution from the Climate Agent) — high UV and
    poor air quality accelerate wrinkle/pigmentation-adjacent metrics
    (modeled here via `wrinkles` and `texture`) if adherence is low

This is a transparent, explainable heuristic model for the prototype —
not a trained time-series model. Swap `_project_one` for a real model
(e.g. an ONNX/PyTorch regressor trained on longitudinal skin imagery)
for production, keeping this function's signature so the rest of the
app doesn't need to change.
"""

from models import SkinMetrics

HORIZONS_DAYS = [7, 30, 90, 180]
LONG_HORIZON_YEARS = 5


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def _project_one(metrics: SkinMetrics, days: float, adherence: float, uv_index: float) -> dict:
    """adherence: 0 (no routine consistency) .. 1 (fully consistent).
    uv_index: 0..11+ from the Climate Agent."""
    import math
    # Saturating curve (not a hard cap at 180d) so the 5-year horizon
    # visibly diverges from the 180-day one instead of flattening out.
    t = 1 - math.exp(-days / 150)
    uv_pressure = min(uv_index / 11, 1.0)

    out = {}
    base = metrics.model_dump()
    for key, val in base.items():
        if key == "hydration":
            # improves with adherence, degrades slowly without it
            delta = (adherence - 0.3) * 0.4 * t
        elif key in ("wrinkles", "texture"):
            # climate pressure pushes these up over time unless adherence offsets it
            delta = (uv_pressure * 0.25 - adherence * 0.3) * t
        else:
            # acne, redness, pores, oiliness, dark_circles: routine adherence improves them
            delta = -(adherence - 0.3) * 0.35 * t
        out[key] = round(_clamp(val + delta), 2)
    return out


def project(metrics: SkinMetrics, habit_streak_days: int, uv_index: float | None) -> dict:
    adherence = min(habit_streak_days / 30, 1.0)
    uv = uv_index if uv_index is not None else 5.0

    timeline = {f"{d}_days": _project_one(metrics, d, adherence, uv) for d in HORIZONS_DAYS}
    timeline["5_years"] = _project_one(metrics, 180 * (LONG_HORIZON_YEARS * 2), adherence, uv)
    timeline["_meta"] = {
        "adherence_score": round(adherence, 2),
        "uv_index_used": uv,
        "note": "Heuristic projection for prototype demo purposes, not a clinical prediction.",
    }
    return timeline
