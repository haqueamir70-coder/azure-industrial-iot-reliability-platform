# Telemetry Contract

## Required envelope

| Field | Type | Rule |
|---|---|---|
| event_id | string | Unique event identifier, used for deduplication |
| schema_version | string | Explicit schema version |
| asset_id | string | Stable equipment identifier |
| site_id | string | Synthetic site identifier |
| event_time | RFC 3339 timestamp | UTC preferred |
| measurements | object | Numeric values with documented units |

## Measurement names and units
- temperature_c: degrees Celsius
- vibration_mm_s: vibration velocity in millimetres per second
- rpm: revolutions per minute
- current_amp: electrical current in amperes

## Validation
Reject or quarantine events with missing identifiers, invalid timestamps, unsupported schema versions, non-finite numeric values, or missing required measurements. Do not silently invent values.

## Compatibility
For additive changes, add optional fields and increment the minor schema version according to the project versioning policy. For breaking changes, introduce a new major schema version and a controlled migration period.
