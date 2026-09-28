from runtime_evidence import runtime_evidence
import time

def test_foundation_contract():
    e=runtime_evidence(request_id="foundation",stage="foundation",decision="DENY",started=time.perf_counter(),error="blocked")
    assert e["decision"] == "DENY"
    assert e["error"] == "blocked"
