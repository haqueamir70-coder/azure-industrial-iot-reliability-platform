from datetime import datetime,timezone
from iot_reliability.models import TelemetryEvent
from iot_reliability.rules import evaluate
def event(temp=30,vibration=1): return TelemetryEvent(event_id="t1",asset_id="M1",asset_type="motor",temperature_c=temp,vibration_mm_s=vibration,timestamp=datetime.now(timezone.utc))
def test_normal(): assert evaluate(event()) is None
def test_warning(): assert evaluate(event(temp=82))[0]=="warning"
def test_critical(): assert evaluate(event(temp=98))[0]=="critical"
