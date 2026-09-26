# Principal Engineering Contract

## Scope
This repository is a production-oriented RAG reference implementation. The evidence chain is enforced by CI and security gates; deployment manifests are hardened consistently across Kubernetes, Helm, and Terraform.

## Core boundary
**Primary concern:** RAG.

Separate retrieval, ranking, generation, and provider adapters; make retrieval failures explicit; validate documents and query contracts; expose provenance/context metadata; keep provider replacement low-cost.

## Non-functional requirements
- **Determinism:** core behavior is reproducible in tests without live external services.
- **Failure semantics:** expected failure classes are explicit and observable; hidden retries are avoided.
- **Security:** validate untrusted inputs, use non-root workloads, drop Linux capabilities, disable privilege escalation, use RuntimeDefault seccomp, and keep deployment images version-pinned.
- **Operability:** expose health/readiness signals and preserve request/correlation context for diagnosis.
- **Change safety:** CI, production tests, dependency audit, and security/SBOM are release gates.

## Evidence checklist
- [x] Public contracts are validated.
- [x] Domain policy is independent from infrastructure adapters.
- [x] Failure and retry behavior is explicit.
- [x] Resource limits are bounded where work can grow.
- [x] Tests cover happy path, invalid input, and representative failure paths.
- [x] Security-sensitive deployment decisions are enforced in Kubernetes, Helm, and Terraform.
- [x] CI validates formatting, lint, typing, tests, coverage, and container build.
- [x] Security/SBOM scans and production tests run on main and pull requests.
- [x] Architecture trade-offs are documented in ADRs.

## Evidence boundary
GREEN means the repository's configured gates pass on the current main commit. It does not mean an environment-independent production certification. Production deployment still requires environment-specific SLOs, capacity planning, secrets management, dependency hardening, and operational ownership.
