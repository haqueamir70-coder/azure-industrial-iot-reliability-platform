import os
from dataclasses import dataclass
@dataclass(frozen=True)
class Settings:
    database_path: str = os.getenv("DATABASE_PATH", "data/iot-alerts.db")
    temperature_warning_c: float = float(os.getenv("TEMP_WARNING_C", "80"))
    temperature_critical_c: float = float(os.getenv("TEMP_CRITICAL_C", "95"))
    vibration_warning_mm_s: float = float(os.getenv("VIBRATION_WARNING_MM_S", "6"))
    vibration_critical_mm_s: float = float(os.getenv("VIBRATION_CRITICAL_MM_S", "10"))
settings = Settings()
