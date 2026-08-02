"""Agent 5 — Climate Agent.

Fetches current UV/humidity/temperature/pollution for the user's city
and adjusts the skincare routine. Wire to a real weather + air-quality
API (e.g. OpenWeather, IQAir) — mocked here for the prototype.
"""

import random


async def get_climate_context(city: str | None) -> dict:
    random.seed(hash(city or "default") % 1000)
    return {
        "city": city or "unknown",
        "uv_index": round(random.uniform(2, 11), 1),
        "humidity_pct": round(random.uniform(30, 90), 1),
        "temperature_c": round(random.uniform(15, 35), 1),
        "pollution_aqi": round(random.uniform(20, 150), 1),
    }


def adjust_routine(routine: list[str], climate: dict) -> list[str]:
    adjusted = list(routine)
    if climate.get("uv_index", 0) >= 7:
        adjusted.append(f"UV index in {climate['city']} is high ({climate['uv_index']}) — reapply SPF midday")
    if climate.get("humidity_pct", 0) < 40:
        adjusted.append("Low humidity detected — add a hydrating mist or richer moisturizer")
    if climate.get("pollution_aqi", 0) > 100:
        adjusted.append(f"Poor air quality (AQI {climate['pollution_aqi']}) — double-cleanse in the evening")
    return adjusted
