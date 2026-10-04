"""Concurrent HTTP retrieval evidence for CI.

Exercises the actual FastAPI retrieval boundary with deterministic queries.
This is a repeatable CI acceptance benchmark, not a production hardware claim.
"""

from __future__ import annotations

import importlib
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
app = importlib.import_module("service").app

CASES = [
    ("security", "security controls encryption audit logging", "security"),
    ("retrieval", "retrieval quality ranking grounded citations", "retrieval"),
    ("observability", "observability traces metrics request evidence", "observability"),
    ("reliability", "reliability retries circuit breakers resilience", "reliability"),
]


def run(repetitions: int = 25, workers: int = 8) -> dict[str, object]:
    if repetitions < 1 or workers < 1:
        raise ValueError("repetitions and workers must be positive")

    work = [(name, query, expected) for _ in range(repetitions) for name, query, expected in CASES]
    latencies: list[float] = []
    failures = 0
    grounded = 0

    def one(case: tuple[str, str, str]) -> tuple[float, bool, bool]:
        name, query, expected = case
        started = time.perf_counter()
        with TestClient(app) as client:
            response = client.post(
                "/v1/retrieve",
                json={
                    "key": name,
                    "payload": {"text": query, "query": expected},
                },
            )
        latency = (time.perf_counter() - started) * 1000
        if response.status_code != 200:
            return latency, False, False
        body = response.json()
        hit = any(
            item.get("document_id") == expected and item.get("score", 0) > 0
            for item in body.get("results", [])
        )
        return latency, True, hit

    wall_started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one, case) for case in work]
        for future in as_completed(futures):
            latency, ok, hit = future.result()
            latencies.append(latency)
            failures += int(not ok)
            grounded += int(hit)
    wall_s = time.perf_counter() - wall_started
    ordered = sorted(latencies)

    def pct(q: float) -> float:
        index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * q)))
        return ordered[index]

    total = len(work)
    return {
        "requests": total,
        "workers": workers,
        "failures": failures,
        "error_rate": failures / total,
        "recall_at_1": grounded / total,
        "throughput_rps": round(total / wall_s, 2),
        "latency_ms": {
            "p50": round(statistics.median(ordered), 3),
            "p95": round(pct(0.95), 3),
            "p99": round(pct(0.99), 3),
        },
        "workload": "FastAPI TestClient -> /v1/retrieve -> chunk/store/search/rerank",
        "measurement": "repeatable CI HTTP retrieval acceptance benchmark; not a production hardware claim",
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
