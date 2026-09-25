# ADR-0001: Separate domain logic from infrastructure

**Status:** Accepted

## Context

AI platforms evolve rapidly and external SDKs are volatile. Coupling domain behavior to infrastructure increases migration and testing cost.

## Decision

Keep domain contracts small and isolate integrations behind adapters.

## Consequences

Improves testability and replacement cost, at the expense of adapter code and explicit translation between external and internal models.
