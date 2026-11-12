from fastapi import FastAPI,Query
from prometheus_client import CONTENT_TYPE_LATEST,Counter,generate_latest
from starlette.responses import Response
from .config import settings
from .models import TelemetryEvent
from .service import TelemetryProcessor
from .storage import AlertStore
app=FastAPI(title="Industrial IoT Reliability API",version="0.1.0",description="Synthetic demo, not for industrial control or safety decisions.")
store=AlertStore(settings.database_path)
processor=TelemetryProcessor(store)
events=Counter("iot_telemetry_events_total","Telemetry events accepted")
alert_counter=Counter("iot_alerts_created_total","Alerts created",["severity"])
@app.get("/healthz")
def health(): return {"status":"ok","mode":"synthetic-demo"}
@app.get("/api/v1/assets")
def assets(): return [{"asset_id":"MOTOR-DEMO-01","asset_type":"motor","site_id":"SITE-DEMO"},{"asset_id":"PUMP-DEMO-01","asset_type":"pump","site_id":"SITE-DEMO"}]
@app.post("/api/v1/telemetry",status_code=202)
def ingest(event:TelemetryEvent):
    events.inc(); alert=processor.process(event)
    if alert: alert_counter.labels(severity=alert.severity).inc()
    return {"accepted":True,"alert_created":alert is not None,"alert":alert}
@app.get("/api/v1/alerts")
def get_alerts(limit:int=Query(default=100,ge=1,le=500)): return store.list(limit)
@app.get("/metrics")
def metrics(): return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
