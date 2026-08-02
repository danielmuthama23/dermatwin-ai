"""Agent 3 — Fashion Intelligence Agent.

Uses skin-tone/redness signals from the twin plus YouCam Apparel VTO to
recommend colors and try on specific garments. Mock recommendations
when YouCam credentials aren't configured.
"""

from models import SkinMetrics
from youcam_client import get_youcam_client


def recommend_colors(metrics: SkinMetrics) -> list[str]:
    picks = []
    if metrics.redness > 0.5:
        picks.append("Cool-toned greens and blues to visually offset redness")
    else:
        picks.append("Warm earth tones (rust, olive, camel) suit your current skin tone")
    if metrics.dark_circles > 0.5:
        picks.append("Avoid stark white near the face; soft ivory reduces under-eye contrast")
    picks.append("Muted jewel tones photograph well against your current complexion")
    return picks


async def try_on(image_bytes: bytes, garment_id: str) -> dict:
    client = get_youcam_client()
    if client is None:
        return {"mode": "mock", "garment_id": garment_id, "preview_url": None,
                "note": "Configure YOUCAM_API_KEY to render a real try-on preview."}
    return await client.virtual_try_on(image_bytes, garment_id)
