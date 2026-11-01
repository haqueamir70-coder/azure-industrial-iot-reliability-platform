# Architecture Decision Records

Use this folder for decisions with context, options, decision, consequences and review date.

## ADR-001: Event-driven ingestion
**Status:** Accepted for reference design

**Context:** Telemetry producers must not depend on synchronous API availability. Data should be buffered and consumed independently.

**Decision:** Use Azure Event Hubs as event ingress.

**Consequences:** Consumers must manage checkpoints, partition ownership, retries and duplicate delivery. Partition count and key strategy require workload sizing.

## ADR-002: Separate operational and analytical workloads
**Status:** Accepted for reference design

**Context:** The API needs low-latency current equipment state, while reliability engineers need historical exploration.

**Decision:** Use an operational store for current state and alert records, and a time-series analytics store for historical telemetry.

**Consequences:** Routing, retention, schema governance and consistency expectations must be explicit.
