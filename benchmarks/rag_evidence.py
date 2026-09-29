"""Deterministic RAG retrieval evidence for CI.

Measures the repository's actual in-memory retrieval path. This is a CI
reference measurement, not a production performance claim.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_domain import Chunk, InMemoryVectorStore, ScoreReranker


CASES = [
    ("security", "security controls encryption audit logging", "security"),
    ("retrieval", "retrieval quality ranking grounded citations", "retrieval"),
    ("observability", "observability traces metrics request evidence", "observability"),
    ("reliability", "reliability retries circuit breakers resilience", "reliability"),
]


def run() -> dict[str, object]:
    chunks = [
        Chunk(document_id=name, text=text, index=0)
        for name, text, _ in CASES
    ]
    store = InMemoryVectorStore()
    store.upsert(chunks)
    reranker = ScoreReranker()

    latencies: list[float] = []
    errors = 0
    hits_at_3 = 0

    for _, query, expected_document in CASES:
        started = time.perf_counter()
        try:
            hits = reranker.rerank(query, store.search(query, top_k=3))
            if any(hit.chunk.document_id == expected_document for hit in hits):
                hits_at_3 += 1
        except Exception:
            errors += 1
        latencies.append((time.perf_counter() - started) * 1000)

    ordered = sorted(latencies)

    def pct(q: float) -> float:
        return ordered[min(len(ordered) - 1, int(len(ordered) * q))]

    return {
        "cases": len(CASES),
        "errors": errors,
        "error_rate": errors / len(CASES),
        "recall_at_3": hits_at_3 / len(CASES),
        "latency_ms": {
            "p50": round(pct(0.50), 3),
            "p95": round(pct(0.95), 3),
        },
        "workload": "InMemoryVectorStore + ScoreReranker",
        "measurement": "CI reference-path retrieval benchmark; not a production performance claim",
    }


def write_report(path: str | Path) -> dict[str, object]:
    report = run()
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return report


if __name__ == "__main__":
    write_report("artifacts/rag-retrieval-evidence.json")
