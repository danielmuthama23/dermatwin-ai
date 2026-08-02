"""Agent 2 — Beauty Scientist Agent.

Turns raw skin metrics + user allergies/goals into a personalized
skincare routine. Rule-based scaffold here; swap `_reason` for a real
LLM call (OpenAI/Claude/Gemini via MCP) that reasons over ingredient
databases and clinical study snippets.
"""

from models import SkinMetrics


def _reason(metrics: SkinMetrics, allergies: list[str]) -> list[str]:
    routine: list[str] = []

    if metrics.hydration < 0.5:
        routine.append("Hyaluronic acid serum, AM & PM, to rebuild barrier hydration")
    if metrics.acne > 0.5:
        routine.append("2% salicylic acid cleanser, PM, to target active breakouts")
    if metrics.redness > 0.5:
        routine.append("Centella asiatica / niacinamide cream, AM, to calm redness")
    if metrics.oiliness > 0.6:
        routine.append("Oil-free gel moisturizer, AM, to balance sebum without stripping")
    if metrics.wrinkles > 0.4:
        routine.append("Low-strength retinal, PM (3x/week to start), for fine-line prevention")
    if metrics.pores > 0.5:
        routine.append("Niacinamide + zinc serum, AM, to refine pore appearance")
    if metrics.dark_circles > 0.5:
        routine.append("Caffeine + vitamin K eye cream, AM & PM")

    if not routine:
        routine.append("Maintenance routine: gentle cleanser, SPF 30+ AM, light moisturizer PM")

    routine.append("Broad-spectrum SPF 30+ every morning, non-negotiable")

    if allergies:
        routine = [
            step for step in routine
            if not any(a.lower() in step.lower() for a in allergies)
        ]
        routine.append(f"Screened against allergies: {', '.join(allergies)}")

    return routine


def build_routine(metrics: SkinMetrics, allergies: list[str] | None = None) -> list[str]:
    return _reason(metrics, allergies or [])
