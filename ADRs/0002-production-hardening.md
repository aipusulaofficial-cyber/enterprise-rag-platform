# ADR-0002: Production hardening boundaries
## Context
HTTP control plane, independently testable domain logic, and external infrastructure.
## Decisions
- FastAPI is the edge contract; domain logic remains dependency-light.
- OpenTelemetry is initialized at startup and can export to a collector.
- Kubernetes owns runtime probes/resources; Helm packages the application.
- Terraform owns infrastructure inputs and outputs.
- Trivy and CycloneDX SBOM checks run in CI.
- Contract and property-based tests protect the public boundary.
- Locust provides repeatable load-test scenarios.
## Trade-offs
Deterministic local execution keeps CI reproducible; production should externalize state, secrets, telemetry, autoscaling, and durable queues.
