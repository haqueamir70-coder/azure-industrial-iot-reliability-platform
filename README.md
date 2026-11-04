# Azure Industrial IoT Reliability Platform

![Azure](https://img.shields.io/badge/Azure-Industrial%20IoT-0078D4?logo=microsoftazure&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![CI](https://github.com/haqueamir70-coder/azure-industrial-iot-reliability-platform/actions/workflows/ci.yml/badge.svg?branch=main)
![Status](https://img.shields.io/badge/Status-Synthetic%20Telemetry%20Lab-orange)

A synthetic-data reference platform for modelling equipment telemetry, event contracts and reliability operations for rotating assets such as motors and pumps.

> **Safety and confidentiality boundary:** This is an independent portfolio lab. It uses generated data only and is not connected to any refinery, customer system, OT network, PLC, safety-instrumented system or real equipment. Demo anomaly thresholds are illustrative software examples—not certified alarm limits, maintenance advice or safety controls.

## What is implemented

- Versioned telemetry contract and JSON Schema at `schemas/telemetry-event.schema.json`.
- Python simulator producing JSON Lines events for synthetic sites and assets.
- Deterministic unit tests for event shape, parameter validation and demo anomaly injection.
- GitHub Actions checks for required documentation, secret scanning, Python compilation and unit tests.
- Azure target architecture and operational runbooks for Event Hubs ingestion, consumer lag, quarantine, alert delivery and SLO design.

## Architecture

![Azure Industrial IoT Architecture](architecture/azure-industrial-iot-architecture.svg)

The target design shows Event Hubs ingestion, stream processing, operational/analytical stores, an equipment API/dashboard, alert evaluation and observability. Cloud adapters and Azure resources are future implementation milestones; this repository does not claim that the target architecture has been deployed.

## Run the synthetic telemetry simulator

Requirements: Python 3.12+; no third-party packages required.

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m src.telemetry_simulator --events 12 --assets 3 --seed 42
```

Inject a synthetic abnormal pattern into every fifth event:

```bash
python -m src.telemetry_simulator --events 20 --assets 4 --anomaly-every 5 > telemetry.jsonl
```

Validate the generated JSON Lines against the schema with your preferred JSON Schema Draft 2020-12 validator. Do not feed generated events into real OT or customer systems.

## Telemetry contract

Each event includes:
- `event_id`: unique UUID for deduplication.
- `schema_version`: explicit contract version.
- `asset_id` and `site_id`: synthetic identifiers.
- `event_time`: timezone-aware RFC 3339 timestamp in UTC.
- `measurements`: temperature (°C), vibration velocity (mm/s), speed (rpm) and current (A).

See [telemetry contract](docs/telemetry-contract.md) and [JSON Schema](schemas/telemetry-event.schema.json).

## Reliability and operational design

The operational guide covers accepted/rejected events, consumer lag, checkpoint age, poison-event quarantine, idempotent alert delivery, latency and data completeness. Example SLOs are learning targets only and must be derived from actual workload requirements before production use.

- [Reliability and operations](docs/reliability-operations.md)
- [Security model](docs/security-model.md)
- [Architecture decisions](architecture/decisions/README.md)
- [Senior interview preparation](interview-prep/README.md)

## Roadmap

1. **Implemented:** telemetry schema, simulator, local unit tests and CI.
2. **Next:** Event Hubs producer/consumer adapters with managed identity and checkpointing.
3. **Next:** event validation, idempotent processing and dead-letter/quarantine flow.
4. **Next:** synthetic equipment-state API, rule engine and dashboard.
5. **Next:** Terraform modules for private Azure baseline and least-privilege identity.
6. **Later:** AKS deployment, dashboards, alert routing, load tests and operational evidence.

## Engineering constraints

- Never commit customer telemetry, site names, credentials, connection strings or secrets.
- Do not send control commands to industrial equipment from this demo.
- Separate IT analytics from OT control and safety systems.
- Treat timestamps, schema compatibility, deduplication and replay semantics as first-class design concerns.
- Mark every cloud component as planned until it has actual deployment and test evidence.

## Author

MD Amirul Haque · [GitHub profile](https://github.com/haqueamir70-coder) · [LinkedIn](https://www.linkedin.com/in/md-amirul-haque/)


## Architecture and interview preparation

See the [architecture diagram and interview questions](docs/README.md) for the repository-specific design walkthrough and technical interview guide.
