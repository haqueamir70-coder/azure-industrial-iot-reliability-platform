# Security Model

## Identity and access
- Prefer Microsoft Entra ID managed identities for Azure workload access.
- Grant only the minimum data-plane roles required by each workload.
- Separate human operator identities from application identities.
- Avoid long-lived client secrets in application configuration and CI.

## Network
- Use private endpoints and private DNS where supported by the selected Azure services and deployment model.
- Restrict public network access where feasible.
- Keep administrative endpoints out of public subnets.
- Treat any connection from an industrial/OT network as a separately reviewed trust boundary; this demo has no OT connectivity.

## Supply chain
- Pin action and dependency versions.
- Scan infrastructure as code and container images.
- Generate and retain build provenance/SBOM as the pipeline matures.
- Require review for production deployment and privileged workflow changes.

## Data
- Use synthetic telemetry only.
- Classify and minimize operational data.
- Define retention and deletion policies.
- Never commit credentials, personal data, customer data or sensitive infrastructure identifiers.

## Safety boundary
This repository is monitoring and decision-support only. It does not implement control loops, trips, interlocks or emergency shutdown logic.
