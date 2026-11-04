import json
import random
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.telemetry_simulator import build_event, generate, is_synthetic_anomaly


class TelemetrySimulatorTests(unittest.TestCase):
    def test_event_matches_documented_contract(self):
        event = build_event(
            "asset-test-001",
            "synthetic-site-001",
            random.Random(7),
            event_time=datetime(2026, 11, 4, 12, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            set(event),
            {"event_id", "schema_version", "asset_id", "site_id", "event_time", "measurements"},
        )
        self.assertEqual(event["schema_version"], "1.0")
        self.assertTrue(event["event_time"].endswith("Z"))
        self.assertEqual(
            set(event["measurements"]),
            {"temperature_c", "vibration_mm_s", "rpm", "current_amp"},
        )

    def test_demo_anomaly_is_detectable(self):
        events = generate(events=4, assets=2, seed=42, anomaly_every=2)
        self.assertFalse(is_synthetic_anomaly(events[0]))
        self.assertTrue(is_synthetic_anomaly(events[1]))
        self.assertFalse(is_synthetic_anomaly(events[2]))
        self.assertTrue(is_synthetic_anomaly(events[3]))

    def test_invalid_generation_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            generate(events=0, assets=1, seed=1, anomaly_every=0)
        with self.assertRaises(ValueError):
            generate(events=1, assets=1, seed=1, anomaly_every=-1)

    def test_schema_is_valid_json_and_documents_required_fields(self):
        schema = json.loads(
            Path("schemas/telemetry-event.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(schema["type"], "object")
        self.assertIn("event_time", schema["required"])
        self.assertIn("measurements", schema["required"])


if __name__ == "__main__":
    unittest.main()
