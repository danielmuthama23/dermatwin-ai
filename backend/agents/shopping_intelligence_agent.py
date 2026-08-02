"""Agent 7 — Shopping Intelligence.

Predicts return probability, satisfaction, and repurchase likelihood
for a recommended product, using how well it matches the user's
current skin/color profile as a proxy signal. Replace `_match_score`
with a trained model over historical purchase/return data.
"""

from models import SkinMetrics


def _match_score(metrics: SkinMetrics, product_tags: list[str]) -> float:
    score = 0.7
    if "sensitive-skin" in product_tags and metrics.redness > 0.5:
        score += 0.15
    if "oil-free" in product_tags and metrics.oiliness > 0.5:
        score += 0.1
    if "hydrating" in product_tags and metrics.hydration < 0.5:
        score += 0.15
    return min(score, 0.98)


def predict(metrics: SkinMetrics, product_tags: list[str]) -> dict:
    match = _match_score(metrics, product_tags)
    return {
        "match_score": round(match, 2),
        "predicted_satisfaction": round(match * 0.95, 2),
        "return_probability": round(max(0.02, 1 - match), 2),
        "repurchase_likelihood": round(match * 0.8, 2),
    }
