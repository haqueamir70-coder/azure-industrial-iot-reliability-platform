#!/usr/bin/env python3
"""Generate synthetic equipment telemetry as JSON Lines.

This simulator is for local engineering tests only. It is not connected to
industrial control systems and its illustrative anomaly thresholds are not
safety limits or maintenance recommendations.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import uuid
from datetime import datetime, timezone
from typing import TextIO


SCHEMA_VERSION = "1.0"


def build_event(
    asset_id: str,
    site_id: str,
    rng: random.Random,
    *,
    event_time: datetime | None = None,
    inject_anomaly: bool = False,
) -> dict[str, object]:
    """Build one event that follows docs/telemetry-contract.md."""
    timestamp = event_time or datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        raise ValueError("event_time must be timezone-aware")

    measurements = {
        "temperature_c": round(rng.uniform(45.0, 72.0) + (35.0 if inject_anomaly else 0), 2),
        "vibration_mm_s": round(rng.uniform(1.0, 4.5) + (6.0 if inject_anomaly else 0), 2),
        "rpm": round(rng.uniform(900.0, 1800.0), 1),
        "current_amp": round(rng.uniform(8.0, 28.0), 2),
    }
    if not all(math.isfinite(value) for value in measurements.values()):
        raise ValueError("generated measurements must be finite")

    return {
        "event_id": str(uuid.uuid4()),
        "schema_version": SCHEMA_VERSION,
        "asset_id": asset_id,
        "site_id": site_id,
        "event_time": timestamp.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "measurements": measurements,
    }


def is_synthetic_anomaly(event: dict[str, object]) -> bool:
    """Apply demo-only thresholds; never use these as certified protection limits."""
    measurements = event["measurements"]
    assert isinstance(measurements, dict)
    return (
        float(measurements["temperature_c"]) >= 85.0
        or float(measurements["vibration_mm_s"]) >= 7.0
    )


def generate(events: int, assets: int, seed: int, anomaly_every: int) -> list[dict[str, object]]:
    if events < 1 or assets < 1:
        raise ValueError("events and assets must both be at least 1")
    if anomaly_every < 0:
        raise ValueError("anomaly_every cannot be negative")

    rng = random.Random(seed)
    output = []
    for index in range(events):
        output.append(
            build_event(
                asset_id=f"asset-{(index % assets) + 1:03d}",
                site_id="synthetic-site-001",
                rng=rng,
                inject_anomaly=anomaly_every > 0 and (index + 1) % anomaly_every == 0,
            )
        )
    return output


def write_jsonl(events: list[dict[str, object]], stream: TextIO) -> None:
    for event in events:
        stream.write(json.dumps(event, separators=(",", ":"), sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=int, default=10, help="number of events to generate")
    parser.add_argument("--assets", type=int, default=3, help="number of synthetic assets")
    parser.add_argument("--seed", type=int, default=42, help="random seed for repeatable measurements")
    parser.add_argument("--anomaly-every", type=int, default=0, help="inject a demo anomaly every Nth event; 0 disables")
    args = parser.parse_args()
    write_jsonl(generate(args.events, args.assets, args.seed, args.anomaly_every), __import__("sys").stdout)


if __name__ == "__main__":
    main()
