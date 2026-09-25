from fastapi.testclient import TestClient

from service import app

client = TestClient(app)


def test_http_contract():
    assert client.get("/health/live").status_code == 200
    response = client.post(
        "/v1/retrieve",
        json={"key": "contract", "payload": {"text": "contract", "query": "contract"}},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_contract():
    assert client.get("/health/ready").json()["status"] == "ready"
