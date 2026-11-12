from datetime import datetime,timezone
from uuid import uuid4
from .models import Alert,TelemetryEvent
from .rules import evaluate
from .storage import AlertStore
class TelemetryProcessor:
    def __init__(self,store:AlertStore): self.store=store
    def process(self,event:TelemetryEvent)->Alert|None:
        decision=evaluate(event)
        if decision is None: return None
        severity,message=decision
        alert=Alert(alert_id=str(uuid4()),event_id=event.event_id,asset_id=event.asset_id,site_id=event.site_id,severity=severity,message=message,created_at=datetime.now(timezone.utc))
        return alert if self.store.add(alert) else None
