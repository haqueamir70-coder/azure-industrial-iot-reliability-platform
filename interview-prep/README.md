# Senior Azure DevOps / DevSecOps Interview Handbook

This handbook accompanies the Azure Industrial IoT Reliability Platform. Answers are concise starting points. Expand them with trade-offs, failure modes, metrics and examples in an interview.

## 1. Architecture and event-driven design

### Q1. Walk me through this platform architecture.
**Answer:** Synthetic equipment producers send versioned telemetry to Event Hubs. Functions validates and enriches events; Stream Analytics demonstrates windowed processing. Cosmos DB supports current-state API reads, while Data Explorer supports historical analytics. FastAPI and a dashboard expose insights. Terraform and GitHub Actions provide repeatable infrastructure and delivery, with security and observability gates.

### Q2. Why use Event Hubs instead of sending every reading directly to an API?
**Answer:** Event Hubs decouples producers from consumers, buffers bursts, supports partitioned parallel consumption and allows multiple independent consumer groups. A synchronous API would tightly couple device availability to application availability and force us to build buffering and fan-out.

### Q3. What is an Event Hubs partition?
**Answer:** A partition is an ordered sequence of events within a hub. Ordering is guaranteed within a partition, not across the whole hub. More partitions enable parallelism, but count and key distribution must match workload needs.

### Q4. How would you choose a partition key?
**Answer:** Use a stable key such as asset ID when events for an individual asset need ordering. Validate cardinality and distribution to avoid hot partitions. Partition count limits parallelism for partitioned consumers.

### Q5. What is a consumer group?
**Answer:** An independent view of an event stream. Different applications can consume the same hub at their own pace using separate groups, such as operational processing and analytics.

### Q6. Explain checkpointing.
**Answer:** A checkpoint records consumer progress, commonly at partition level. After restart or reassignment, a consumer resumes from its stored position. Frequency trades recovery replay against checkpoint overhead.

### Q7. Does Event Hubs guarantee exactly-once processing end to end?
**Answer:** Do not assume end-to-end exactly-once semantics. Design for at-least-once delivery and make side effects idempotent using stable event IDs, deduplication state and transactional boundaries where supported.

### Q8. How do you handle duplicate telemetry?
**Answer:** Give each event a stable unique ID. Before a side effect, verify whether it was processed already or use a deterministic key. Define the deduplication retention window and monitor duplicates.

### Q9. What is a poison message?
**Answer:** A message that repeatedly fails due to malformed content or an unsupported condition. Apply bounded retries, record failure metadata, quarantine it, alert owners and support controlled replay after remediation.

### Q10. Azure Functions vs Stream Analytics?
**Answer:** Functions suits code-driven event handling, enrichment, integration and custom business logic. Stream Analytics suits declarative temporal windows and continuous aggregations. Choose based on complexity, latency, connectors, scale and operational model.

## 2. Azure data and reliability

### Q11. Why separate operational and analytical storage?
**Answer:** The API needs low-latency reads of current asset status and alerts. Reliability analysis needs efficient scans, aggregations and time-series exploration. Separate stores let each workload use an appropriate model and scaling profile.

### Q12. What belongs in Cosmos DB?
**Answer:** Current asset state, latest measurements, alert metadata and API-oriented documents. Partition keys should align with access patterns and distribute load. Retention and consistency requirements must be explicit.

### Q13. What belongs in Azure Data Explorer?
**Answer:** High-volume time-series telemetry, historical trends, aggregations and exploratory queries. It helps engineers correlate readings over time across assets.

### Q14. How do you build a resilient consumer?
**Answer:** Use bounded retries with exponential backoff and jitter, idempotent writes, checkpointing, poison-event isolation, health probes and scale based on lag. Test restart, duplicate delivery and downstream outage scenarios.

### Q15. How do you prevent data loss during a downstream outage?
**Answer:** Keep durable ingress buffering, avoid checkpointing before successful processing, size retention for recovery objectives, use retry/quarantine strategies and monitor lag against retention. Test recovery with fault injection.

### Q16. How do you avoid alert storms?
**Answer:** Use severity thresholds with hysteresis, deduplication keys, cooldown periods, grouping by asset and incident correlation. Make rules configurable and version controlled. Measure false positives and missed detections.

### Q17. How would you build anomaly detection?
**Answer:** Start with explainable rules and asset-specific baselines; validate using representative labelled or simulated data. Evaluate precision, recall, false-positive rate and detection delay. Treat model output as advisory until reviewed.

### Q18. What is back-pressure?
**Answer:** Incoming work exceeds downstream processing capacity. Monitor lag and queue depth, control concurrency, scale consumers, optimize slow dependencies and use bounded buffers. Avoid unbounded retries.

### Q19. How do you design replay?
**Answer:** Retain original event IDs and timestamps, record processing version, and define a replay source and time range. Replay into an isolated or idempotent path, suppress duplicate notifications, and compare output counts and state.

### Q20. What metrics matter?
**Answer:** Ingress rate, rejected events, consumer lag, oldest-event age, processing latency, retry/quarantine count, API p95/p99 latency, error rate, saturation, alert delivery latency and data freshness.

## 3. Terraform and infrastructure as code

### Q21. Why Terraform?
**Answer:** Terraform provides declarative, reviewable and repeatable infrastructure provisioning with reusable modules, plans and state tracking.

### Q22. Explain Terraform state.
**Answer:** State maps configuration resources to real infrastructure and stores attributes required for planning. Protect it with remote storage, encryption, access control, versioning and locking where supported.

### Q23. Why use a remote backend?
**Answer:** It centralizes state for team collaboration, supports access control and can provide locking and recovery. Never commit state files containing sensitive values.

### Q24. What is state locking?
**Answer:** Locking prevents concurrent operations from changing the same state simultaneously. It reduces race conditions and corruption. Never force-unlock without diagnosing the active operation.

### Q25. Plan vs apply?
**Answer:** Plan previews proposed actions from configuration, state and provider reads. Apply executes the approved plan. In CI/CD, review a saved plan and apply the exact reviewed artifact.

### Q26. How do you structure Terraform modules?
**Answer:** Group reusable capabilities behind clear inputs, outputs and version constraints. Keep environment composition in root modules and avoid over-abstracting simple resources.

### Q27. How do you manage secrets in Terraform?
**Answer:** Avoid hardcoding secrets in configuration or tfvars. Prefer workload identities and secret managers. Marking a variable sensitive hides some output but does not guarantee the value is absent from state.

### Q28. How do you detect drift?
**Answer:** Run scheduled plans, review unexpected changes and reconcile intentional changes into code. Do not automatically apply drift remediation without impact assessment.

### Q29. count vs for_each?
**Answer:** count creates indexed instances; for_each creates instances keyed by stable map keys or set values. for_each is often safer when individual resources need stable identity.

### Q30. How do you handle provider upgrades?
**Answer:** Constrain compatible versions, commit the dependency lock file, read upgrade notes, test in a non-production environment and review plans for breaking changes.

## 4. Azure networking and identity

### Q31. What is a private endpoint?
**Answer:** It provides a private IP in a virtual network for accessing a supported Azure service over Private Link. DNS must resolve the service hostname to the private endpoint IP.

### Q32. Why is private DNS important?
**Answer:** Private endpoint connectivity depends on name resolution. Misconfigured DNS can send clients to public endpoints or cause connection failures.

### Q33. What is a managed identity?
**Answer:** An Azure-managed identity lets an application authenticate to supported services without storing credentials in application configuration.

### Q34. Managed identity vs service principal?
**Answer:** Managed identity lifecycle is managed by Azure and avoids credential management. A service principal is an application identity usable across contexts but may require credential or federation management. Prefer managed identity on supported Azure resources.

### Q35. Explain Azure RBAC.
**Answer:** RBAC authorizes actions through role assignments combining a security principal, role definition and scope. Apply least privilege at the narrowest practical scope and distinguish management-plane from data-plane permissions.

### Q36. What is hub-and-spoke networking?
**Answer:** A hub centralizes shared services such as firewall, VPN/ExpressRoute and DNS, while spokes isolate workloads. Peering, routing, security controls and DNS must be designed deliberately.

### Q37. How would you secure Event Hubs access?
**Answer:** Prefer managed identities and narrowly scoped data-plane roles, private connectivity where appropriate, network restrictions, diagnostic logs and secretless deployment. Separate producer and consumer permissions.

### Q38. Troubleshoot private endpoint connectivity?
**Answer:** Validate routes, NSG/UDR rules, private DNS zone links and records, name resolution from the client subnet, TLS hostname and service network settings. Test DNS and TCP independently.

## 5. Containers and Kubernetes

### Q39. Why containerize the API?
**Answer:** Containers package application and runtime dependencies consistently across developer machines, CI and deployment environments. They improve portability but still require image security and observability.

### Q40. Deployment vs StatefulSet?
**Answer:** Deployment manages interchangeable stateless replicas. StatefulSet provides stable identities and ordered deployment/scaling for workloads needing stable identity or persistent storage associations.

### Q41. Readiness vs liveness probes?
**Answer:** Readiness determines whether a pod receives traffic. Liveness determines whether it should restart. Startup probes protect slow-starting apps from premature liveness failures.

### Q42. What is CrashLoopBackOff?
**Answer:** Kubernetes repeatedly restarts a container that exits. Check events, previous logs, exit code, command, configuration, secrets, probes, permissions and resource limits.

### Q43. Requests vs limits?
**Answer:** Requests influence scheduling and represent expected allocation. Limits cap usage; CPU can be throttled and memory overuse can trigger OOM termination. Set them from measured load.

### Q44. How does HPA work?
**Answer:** Horizontal Pod Autoscaler adjusts replicas based on metrics such as CPU, memory or custom metrics. Ensure metrics are available and scale behaviour is appropriate.

### Q45. How would you secure AKS workloads?
**Answer:** Use Entra ID integration, least-privilege RBAC, workload identity, network policies, restricted pod security settings, image scanning, secret management and admission policies.

### Q46. What is Kubernetes NetworkPolicy?
**Answer:** It defines allowed pod ingress and egress when supported by the network plugin. Start with default-deny and add narrowly scoped flows while validating DNS.

### Q47. Debug an unreachable service?
**Answer:** Check endpoints and selectors, pod readiness, service port/targetPort, DNS, NetworkPolicy, ingress/controller, routes and application listener. Inspect events and logs.

### Q48. How do you roll back?
**Answer:** Use a known-good image digest and deployment revision, roll back through the approved pipeline, validate readiness and service metrics, and preserve incident evidence. Plan database changes for backward compatibility.

## 6. CI/CD and DevSecOps

### Q49. Describe a secure CI/CD pipeline.
**Answer:** Checkout pinned code, lint and test, build an immutable image, scan dependencies and image, validate Terraform, run IaC and policy scans, publish provenance, deploy to test, run integration tests and require protected approval before production.

### Q50. Why immutable artifacts?
**Answer:** Build once and promote the same image digest between environments. This prevents rebuild differences and improves rollback and provenance.

### Q51. Purpose of OIDC federation in GitHub Actions?
**Answer:** It lets workflows obtain short-lived cloud credentials instead of storing long-lived Azure client secrets. Restrict trust to the intended repository, branch, environment and audience.

### Q52. What is an SBOM?
**Answer:** A software bill of materials lists components and dependencies in an artifact. It supports vulnerability response, license review and supply-chain visibility.

### Q53. Checkov vs Trivy?
**Answer:** Checkov focuses on IaC and cloud configuration policy scanning. Trivy scans container images, filesystems, dependencies and supported IaC. Use tools for their intended coverage.

### Q54. How should Actions secrets be handled?
**Answer:** Prefer OIDC federation. Scope unavoidable secrets to environments, mask output, limit workflow permissions and never echo credentials or write them to artifacts.

### Q55. Secure GitHub Actions permissions?
**Answer:** Set least-privilege workflow/job permissions, pin third-party actions to full commit SHAs, protect main, require reviews for workflow changes and restrict deployment environments.

### Q56. What is policy as code?
**Answer:** Policy as code expresses guardrails in version-controlled tests evaluated in CI or admission. It makes compliance repeatable and blocks risky changes before deployment.

### Q57. Prevent secrets leaking in Terraform plan artifacts?
**Answer:** Treat plans as sensitive, restrict artifact access and retention, encrypt storage and avoid publishing them to public logs. Prefer designs that keep secret values out of state.

### Q58. What if a security scan fails?
**Answer:** Triage severity and exploitability, identify affected components, fix or upgrade, rerun scans and add regression controls. Exceptions need owner, rationale, compensating controls and expiry.

## 7. Observability and SRE

### Q59. Logs vs metrics vs traces?
**Answer:** Logs capture discrete events, metrics summarize numeric behaviour over time, and traces follow an operation across components. Correlate with trace and asset IDs without leaking sensitive data.

### Q60. What is an SLI?
**Answer:** A measured signal of service behaviour, such as successful request ratio or event processing latency.

### Q61. What is an SLO?
**Answer:** A target for an SLI over a defined window, such as 99.9% successful API requests over 30 days.

### Q62. What is an SLA?
**Answer:** A formal service commitment, often with customer-facing consequences. An SLO is a reliability target; an SLA may specify remedies if breached.

### Q63. What is an error budget?
**Answer:** The permitted unreliability implied by an SLO over its measurement window. Consumption helps teams balance feature delivery and reliability work.

### Q64. How would you monitor consumer lag?
**Answer:** Export lag and oldest-event age by hub, group and partition; alert on sustained growth tied to retention and freshness objectives. Correlate with processing latency and ingress throughput.

### Q65. Design actionable alerts.
**Answer:** Alert on user impact or clear symptoms, require sustained thresholds, include context and runbook links, assign owners and avoid duplicate notifications. Review noise and missed incidents.

### Q66. Prometheus vs Azure Monitor?
**Answer:** Prometheus is a metrics collection/query ecosystem commonly used for Kubernetes and applications. Azure Monitor provides Azure-native metrics, logs, alerts and platform integration. They can complement each other with clear ownership.

### Q67. What is a golden signal?
**Answer:** Common signals are latency, traffic, errors and saturation. For event processing, include consumer lag and data freshness.

### Q68. How do you run a blameless postmortem?
**Answer:** Document impact, timeline, detection, contributing conditions, recovery, root causes and measurable follow-ups. Focus on system conditions rather than individual blame.

## 8. Production scenarios

### Q69. Ingestion is normal but dashboards are stale. What do you check?
**Answer:** Compare event timestamps, ingress metrics, consumer lag, processor errors, store write latency and API query/cache behaviour. Trace one event ID through each stage.

### Q70. One partition has much higher lag. Why?
**Answer:** A skewed key, unusually busy asset, uneven workload or slow consumer can create a hot partition. Inspect key distribution and per-partition throughput.

### Q71. Cosmos DB throttling increases. What next?
**Answer:** Check request charge, hot partition keys, throughput, query patterns and retry-after handling. Optimize partitioning and queries before simply increasing throughput.

### Q72. New deployment increases p99 latency. What do you do?
**Answer:** Compare release markers and traces, inspect dependency latency, resource saturation, connection pools and query plans. Roll back if impact is material, then reproduce and test a fix.

### Q73. Terraform apply partially fails. How recover?
**Answer:** Inspect the error and current state, verify which resources were created, correct the cause and run a fresh plan. Avoid blind destroy/reapply; import or state repair only with a reviewed recovery plan.

### Q74. A secret is committed to Git. What do you do?
**Answer:** Revoke or rotate it immediately, inspect audit logs, remove it from active configuration, then clean history if required. History rewriting does not replace rotation.

### Q75. Cluster is healthy but requests fail. Why?
**Answer:** Cluster health does not prove application-path health. Check service endpoints, ingress, DNS, TLS, network policy, identity, dependencies and app logs.

### Q76. How handle a regional Azure outage?
**Answer:** Define RTO/RPO, identify regional dependencies and replication, maintain tested IaC for recovery, and document traffic failover and data consistency. Validate with game days.

### Q77. Prevent duplicate alerts after replay?
**Answer:** Use a deterministic alert key from asset, rule and event/window; persist alert state; separate replay from live notification; test repeated processing for idempotency.

### Q78. Telemetry arrives out of order. What then?
**Answer:** Preserve event time separately from ingestion time, use event-time windows and define allowed lateness and correction policies. Arrival order is not measurement order.

### Q79. Producer sends malformed payloads at high volume. What do you do?
**Answer:** Validate at processing boundaries, quarantine invalid payloads with reason codes, protect the main consumer, rate-limit abusive producers where possible and alert on rejection spikes.

### Q80. Validate recovery after consumer outage?
**Answer:** Measure backlog before and after, ensure lag falls, compare accepted/processed counts, verify ordering and deduplication, and check freshness and alert latency against objectives.

## 9. Leadership and design discussions

### Q81. Estimate Event Hubs capacity.
**Answer:** Measure average and peak event size/rate, producers and consumers, retention, partitions, burst patterns and protocol overhead. Load-test realistic payloads and validate current service limits and pricing.

### Q82. Choose retention.
**Answer:** Base it on maximum outage/recovery duration, replay requirements, throughput and cost. Retention should exceed the recovery objective with margin.

### Q83. Design environment strategy.
**Answer:** Separate dev, test and production resource boundaries where practical. Use reusable modules, environment-specific variables, independent state, protected approvals and policy guardrails.

### Q84. Introduce this platform to an industrial environment.
**Answer:** Start with architecture and safety reviews, data classification, network segmentation, asset inventory and threat modelling. Run a non-production read-only pilot, validate data quality and failure modes, define ownership, and expand only after formal approval.

### Q85. What to present in an architecture review?
**Answer:** Business problem, requirements/NFRs, diagrams, data flow, trust boundaries, failure modes, scaling assumptions, cost drivers, DR strategy, operational model, risks and decisions.

### Q86. Manage technical debt?
**Answer:** Make it visible, quantify delivery/reliability impact, prioritize by risk and frequency, allocate capacity and define measurable exit criteria.

### Q87. Handle architecture disagreement?
**Answer:** Align on requirements, compare options against measurable criteria, record trade-offs in an ADR, prototype high-risk assumptions and revisit based on evidence.

### Q88. Explain an incident to leadership.
**Answer:** Lead with impact, duration, current status, mitigation and next update. Follow with verified cause and prevention actions; distinguish facts from hypotheses.

### Q89. What makes a good cutover plan?
**Answer:** Explicit entry criteria, data sync, freeze window, owner matrix, validation, communication, go/no-go authority, rollback triggers and tested rollback steps.

### Q90. Prioritize reliability improvements?
**Answer:** Use incidents, SLO/error-budget consumption, customer impact, failure probability, blast radius and effort. Prioritize systemic fixes over repeated manual workarounds.

## 10. Practical exercises

1. Design partitioning for 20,000 synthetic assets with uneven event rates.
2. Implement a consumer that safely handles duplicate IDs and retries.
3. Test late, malformed and out-of-order telemetry.
4. Create Terraform modules for network, private endpoint and monitoring baseline.
5. Add Actions pipeline with least-privilege permissions and security scans.
6. Deploy API to AKS with probes, resource requests/limits and network policy.
7. Dashboard event throughput, oldest-event age and processing failures.
8. Simulate consumer outage and demonstrate safe replay without duplicate alerts.

## Senior-level answer structure

Use: **Context → Decision → Trade-off → Failure mode → Monitoring → Outcome**. Do not claim production experience with components you have only studied or built in a lab. Distinguish implemented work from proposed architecture.
