# Architecture

## System boundary

Public contracts are separated from domain logic and infrastructure adapters. External services can be replaced without changing core behavior.

## Reliability model

Failures are explicit, inputs are validated, and resource usage is bounded at service boundaries. Retries are not hidden inside business logic because retry safety depends on idempotency and workload semantics.

## Production trade-offs

The initial implementation favors simplicity and deterministic local execution over infrastructure-heavy dependencies. Production deployments should externalize shared state, export telemetry through OpenTelemetry, and enforce resource, security, and SLO policies.

## Extension points

Add provider adapters, persistent state, distributed coordination, telemetry exporters, authentication/authorization, and workload-specific scaling without changing core interfaces.
