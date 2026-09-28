import time

from runtime_evidence import runtime_evidence


def test_foundation_contract():
    evidence = runtime_evidence(
        request_id="foundation",
        stage="foundation",
        decision="DENY",
        started=time.perf_counter(),
        error="blocked",
    )
    assert evidence["decision"] == "DENY"
    assert evidence["error"] == "blocked"
