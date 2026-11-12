from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class TelemetryEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(min_length=1, max_length=128)
    asset_id: str = Field(min_length=1, max_length=128)
    asset_type: Literal["motor", "pump"]
    site_id: str = Field(default="SITE-DEMO", min_length=1, max_length=64)
    temperature_c: float = Field(ge=-40, le=250)
    vibration_mm_s: float = Field(ge=0, le=200)
    timestamp: datetime
    @field_validator("timestamp")
    @classmethod
    def timezone_required(cls, value: datetime) -> datetime:
        if value.tzinfo is None: raise ValueError("timestamp must include timezone")
        return value.astimezone(timezone.utc)

class Alert(BaseModel):
    alert_id: str
    event_id: str
    asset_id: str
    site_id: str
    severity: Literal["warning", "critical"]
    message: str
    created_at: datetime
