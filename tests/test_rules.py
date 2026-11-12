from datetime import datetime, timezone

from iot_reliability.models import TelemetryEvent
from iot_reliability.rules import evaluate


def make_event(temp=30, vibration=1):
    return TelemetryEvent(event_id="test-1", asset_id="MOTOR-1", asset_type="motor",
                          temperature_c=temp, vibration_mm_s=vibration,
                          timestamp=datetime.now(timezone.utc))


def test_normal_event_has_no_alert():
    assert evaluate(make_event()) is None


def test_warning_threshold():
    assert evaluate(make_event(temp=82))[0] == "warning"


def test_critical_threshold():
    assert evaluate(make_event(temp=98))[0] == "critical"
