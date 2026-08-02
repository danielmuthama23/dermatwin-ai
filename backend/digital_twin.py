"""
Digital Twin Engine.

Holds the persistent, continuously-updated model of a user (skin state,
routine, wardrobe recommendations, climate context, habits) that every
agent reads from and writes back to. In-memory dict for the hackathon
prototype — swap for PostgreSQL + Redis (as listed in the architecture)
for anything beyond a demo.
"""

from datetime import datetime, timezone
from models import DigitalTwinState

_TWINS: dict[str, DigitalTwinState] = {}


def get_twin(user_id: str) -> DigitalTwinState:
    if user_id not in _TWINS:
        _TWINS[user_id] = DigitalTwinState(user_id=user_id)
    return _TWINS[user_id]


def update_twin(user_id: str, **fields) -> DigitalTwinState:
    twin = get_twin(user_id)
    for key, value in fields.items():
        if hasattr(twin, key) and value is not None:
            setattr(twin, key, value)
    twin.last_updated = datetime.now(timezone.utc).isoformat()
    _TWINS[user_id] = twin
    return twin
