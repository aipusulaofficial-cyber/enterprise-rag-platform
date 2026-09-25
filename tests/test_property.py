from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app

client = TestClient(app)


@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cs",),  # type: ignore[arg-type]
        ),
        min_size=1,
        max_size=64,
    ).filter(lambda value: bool(value.strip()))
)
def test_request_key_never_crashes(value: str):
    response = client.post(
        "/v1/retrieve",
        json={"key": value, "payload": {"text": value, "query": value}},
    )
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "ok"
