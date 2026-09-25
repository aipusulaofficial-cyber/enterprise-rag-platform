# Failure matrix

| Failure | Detection | Action | Retry? | User impact |
|---|---|---|---|---|
| Invalid/untrusted input | contract validation | reject deterministically | No | 4xx |
| Dependency timeout | timeout budget | normalize + record dependency | Only if safe/idempotent | explicit dependency error/degradation |
| Dependency 5xx | provider adapter | bounded exponential backoff | Only if safe/idempotent | bounded latency |
| Repeated dependency failure | circuit breaker | open circuit | No while open | fast failure |
| Local overload | semaphore/token bucket | fail fast | No | 429/degraded path |
| Telemetry failure | exporter error | preserve domain result | bounded/exporter-local only | no domain corruption |

Invalid document/query -> 400; retrieval dependency timeout -> bounded retry only when safe; repeated dependency failures -> degrade to empty-result/explicit dependency failure rather than fabricate context.