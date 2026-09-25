from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from service import app
@given(st.text(min_size=1,max_size=64))
def test_request_key_never_crashes(value):
 r=TestClient(app).post("/v1/retrieval",json={"query":value})
 assert r.status_code==200
