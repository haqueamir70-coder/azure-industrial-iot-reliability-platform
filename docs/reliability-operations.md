# Reliability and Operations

## Golden signals
- Ingestion: events accepted per second and rejected events.
- Consumer health: lag, checkpoint age and partition ownership changes.
- Processing: end-to-end latency, retry count and poison-event count.
- API: request rate, error rate, latency and saturation.
- Alerting: evaluation latency, deduplication count and notification failures.

## Example service objectives
These are learning targets only; validate them against a real workload before use.

| Indicator | Illustrative objective |
|---|---|
| Telemetry processing latency | 99% of accepted events processed within 60 seconds |
| API availability | 99.9% monthly successful health/API requests |
| Alert evaluation | 99% of eligible events evaluated within 30 seconds |
| Data completeness | At least 99.5% of expected simulator events observed |

## Incident runbook: rising consumer lag
1. Confirm affected hub, consumer group, partitions and time window.
2. Check incoming event rate and partition distribution.
3. Review processor errors, throttling, restarts and dependency latency.
4. Check for poison events repeatedly blocking a partition.
5. Scale consumers within partition and service limits; remove bottlenecks first.
6. Preserve failed payload metadata in a quarantine/dead-letter path.
7. Verify lag is falling and event freshness has recovered.
8. Record timeline, impact, root cause and prevention actions.

## Incident runbook: alert delivery delay
1. Compare event, ingestion, evaluation and notification timestamps.
2. Check processor lag and alert-engine queue depth.
3. Check deduplication/idempotency behaviour.
4. Inspect notification adapter failures and rate limits.
5. Retry safely and verify no duplicate external notification was emitted.
6. Document impact and corrective actions.
