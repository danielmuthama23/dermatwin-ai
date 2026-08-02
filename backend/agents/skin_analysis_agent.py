"""Agent 1 — Skin Analysis Agent.

Calls YouCam Skin AI on a selfie and normalizes the result into
SkinMetrics. Falls back to a mock result if no YouCam credentials are
configured, so the rest of the pipeline stays demoable offline.
"""

import random
from typing import Any
from models import SkinMetrics
from youcam_client import YouCamError, get_youcam_client


def _mock_skin_metrics(seed: int) -> SkinMetrics:
    random.seed(seed)
    return SkinMetrics(
        acne=round(random.uniform(0, 1), 2),
        wrinkles=round(random.uniform(0, 1), 2),
        redness=round(random.uniform(0, 1), 2),
        hydration=round(random.uniform(0.3, 1), 2),
        texture=round(random.uniform(0, 1), 2),
        pores=round(random.uniform(0, 1), 2),
        oiliness=round(random.uniform(0, 1), 2),
        dark_circles=round(random.uniform(0, 1), 2),
    )


async def analyze(image_bytes: bytes) -> SkinMetrics:
    client = get_youcam_client()

    if client is None:
        # Mock mode — no valid YouCam configuration available.
        return _mock_skin_metrics(len(image_bytes))

    try:
        raw = await client.analyze_skin(image_bytes)
    except YouCamError:
        return _mock_skin_metrics(len(image_bytes))

    scores = raw.get("data", {}).get("results", raw.get("result", raw))
    if isinstance(scores, list):
        scores = {item.get("name"): item.get("value") for item in scores if isinstance(item, dict)}
    if not isinstance(scores, dict):
        raise RuntimeError("YouCam returned an unsupported skin-analysis response")

    def score(*names: str) -> float:
        value: Any = next((scores[name] for name in names if name in scores), 0)
        if isinstance(value, dict):
            value = value.get("score", value.get("value", 0))
        try:
            number = float(value)
        except (TypeError, ValueError):
            return 0.0
        return round(max(0.0, min(number / 100 if number > 1 else number, 1.0)), 3)

    return SkinMetrics(
        acne=score("acne"),
        wrinkles=score("wrinkle", "wrinkles"),
        redness=score("redness"),
        hydration=score("moisture", "hydration"),
        texture=score("texture"),
        pores=score("pore", "pores"),
        oiliness=score("oiliness"),
        dark_circles=score("dark_circle_v2", "dark_circles", "eye_bag"),
    )
