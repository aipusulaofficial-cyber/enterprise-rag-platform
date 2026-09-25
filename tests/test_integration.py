from fastapi.testclient import TestClient

from service import app


def test_http_contract_and_domain():
    c = TestClient(app)
    assert c.get("/health/live").status_code == 200
    r = c.post(
        "/v1/retrieve",
        json={
            "key": "integration",
            "payload": {"text": "alpha beta", "query": "alpha"},
        },
    )
    assert r.status_code == 200, r.text
