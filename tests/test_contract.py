from fastapi.testclient import TestClient
from service import app
def test_http_contract():
 c=TestClient(app);assert c.get("/health/live").status_code==200
 r=c.post("/v1/retrieval",json={"query":"contract","payload":{}})
 assert r.status_code==200 and r.json()["status"]=="accepted"
def test_readiness_contract(): assert TestClient(app).get("/health/ready").json()["status"]=="ready"
