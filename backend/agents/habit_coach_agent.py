"""Agent 6 — Habit Coach.

Tracks routine adherence, sleep, water intake, and rewards consistency
with streaks/badges. In-memory log for the prototype.
"""

_LOGS: dict[str, list[dict]] = {}


def log_checkin(user_id: str, routine_done: bool, water_glasses: int, sleep_hours: float) -> dict:
    entry = {"routine_done": routine_done, "water_glasses": water_glasses, "sleep_hours": sleep_hours}
    _LOGS.setdefault(user_id, []).append(entry)

    history = _LOGS[user_id]
    streak = 0
    for e in reversed(history):
        if e["routine_done"]:
            streak += 1
        else:
            break

    badge = None
    if streak >= 30:
        badge = "🏆 30-Day Consistency Champion"
    elif streak >= 7:
        badge = "🔥 7-Day Streak"

    return {"streak_days": streak, "badge": badge, "total_checkins": len(history)}


def get_streak(user_id: str) -> int:
    history = _LOGS.get(user_id, [])
    streak = 0
    for e in reversed(history):
        if e["routine_done"]:
            streak += 1
        else:
            break
    return streak
