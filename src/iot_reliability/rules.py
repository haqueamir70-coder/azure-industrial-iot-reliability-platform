from .config import settings
from .models import TelemetryEvent

def evaluate(event:TelemetryEvent)->tuple[str,str]|None:
    """Illustrative demo thresholds only; never use operationally."""
    critical=event.temperature_c>=settings.temperature_critical_c or event.vibration_mm_s>=settings.vibration_critical_mm_s
    warning=event.temperature_c>=settings.temperature_warning_c or event.vibration_mm_s>=settings.vibration_warning_mm_s
    if critical: return "critical",f"Demo critical: temp={event.temperature_c:.1f} C, vibration={event.vibration_mm_s:.1f} mm/s"
    if warning: return "warning",f"Demo warning: temp={event.temperature_c:.1f} C, vibration={event.vibration_mm_s:.1f} mm/s"
    return None
