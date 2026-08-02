from typing import Optional
from pydantic import BaseModel, Field


class SkinMetrics(BaseModel):
    acne: float = 0.0
    wrinkles: float = 0.0
    redness: float = 0.0
    hydration: float = 0.0
    texture: float = 0.0
    pores: float = 0.0
    oiliness: float = 0.0
    dark_circles: float = 0.0


class UserProfile(BaseModel):
    user_id: str
    city: Optional[str] = None
    allergies: list[str] = Field(default_factory=list)
    skin_type: Optional[str] = None
    goals: list[str] = Field(default_factory=list)


class UserAccount(BaseModel):
    user_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    provider: str = "local"
    password_hash: Optional[str] = None
    password_salt: Optional[str] = None
    oauth_id: Optional[str] = None
    city: Optional[str] = None
    allergies: list[str] = Field(default_factory=list)
    skin_type: Optional[str] = None
    goals: list[str] = Field(default_factory=list)
    created_at: Optional[str] = None
    is_active: bool = True


class DigitalTwinState(BaseModel):
    user_id: str
    skin_metrics: Optional[SkinMetrics] = None
    skincare_routine: list[str] = Field(default_factory=list)
    outfit_recommendations: list[str] = Field(default_factory=list)
    climate_context: Optional[dict] = None
    habit_streak_days: int = 0
    predicted_timeline: Optional[dict] = None
    last_updated: Optional[str] = None
