import time

from runtime_evidence import runtime_evidence


def test_platform_contract_smoke():
    evidence = runtime_evidence(request_id="test-request", stage="test", decision="ALLOW", started=time.perf_counter())
    assert evidence["request_id"] == "test-request"
    assert evidence["decision"] == "ALLOW"
    assert evidence["latency_ms"] >= 0
