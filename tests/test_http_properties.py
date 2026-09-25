from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app

client = TestClient(app)


def test_contract():
    assert client.get("/health/live").status_code == 200


@given(st.text(min_size=1, max_size=32))
def test_property(value: str):
    response = client.post(
        "/v1/retrieve",
        json={"key": value, "payload": {"text": value, "query": value}},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["results"], list)
