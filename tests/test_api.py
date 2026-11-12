from datetime import datetime, timezone

from fastapi.testclient import TestClient

from iot_reliability.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_assets_endpoint():
    response = client.get("/api/v1/assets")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_invalid_event_is_rejected():
    payload = {"event_id": "invalid", "asset_id": "MOTOR-1", "asset_type": "motor",
               "temperature_c": 999, "vibration_mm_s": 1,
               "timestamp": datetime.now(timezone.utc).isoformat()}
    assert client.post("/api/v1/telemetry", json=payload).status_code == 422
