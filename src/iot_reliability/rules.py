from .config import settings
from .models import TelemetryEvent


def evaluate(event: TelemetryEvent) -> tuple[str, str] | None:
    """Illustrative demo thresholds only; never use these values operationally."""
    critical = (event.temperature_c >= settings.temperature_critical_c
                or event.vibration_mm_s >= settings.vibration_critical_mm_s)
    warning = (event.temperature_c >= settings.temperature_warning_c
               or event.vibration_mm_s >= settings.vibration_warning_mm_s)
    if critical:
        return "critical", (f"Demo threshold exceeded: temperature={event.temperature_c:.1f} C, "
                             f"vibration={event.vibration_mm_s:.1f} mm/s")
    if warning:
        return "warning", (f"Demo warning threshold reached: temperature={event.temperature_c:.1f} C, "
                            f"vibration={event.vibration_mm_s:.1f} mm/s")
    return None
