# Architecture Overview

## Goal
Build a decoupled telemetry-to-insight flow for synthetic rotating-equipment assets. The platform separates event ingestion, stream processing, operational state, analytics, and user-facing APIs.

## Logical flow
1. The simulator emits versioned telemetry events with unique event IDs and UTC timestamps.
2. Azure Event Hubs provides durable event ingress and partitioned streams.
3. Azure Functions validates, enriches and routes events with idempotent operational updates.
4. Azure Stream Analytics demonstrates windowed processing and real-time routing.
5. Cosmos DB stores current asset state and alert records for the API.
6. Azure Data Explorer stores and queries historical telemetry for trend analysis.
7. FastAPI exposes equipment, telemetry, health and alert endpoints.
8. A dashboard presents current state, trends and acknowledged alerts.
9. Azure Monitor / Application Insights and Prometheus/Grafana provide observability.

## Trust boundaries
- Device/simulator to cloud ingress
- Event processor identity to data stores
- API identity to operational data
- CI identity to deployment target
- Operator access to dashboards and cloud resources

Use managed identities, least-privilege roles, private networking where appropriate, and auditable deployments. This demo has no OT network connectivity.
