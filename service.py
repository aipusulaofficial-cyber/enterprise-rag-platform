"""Production HTTP surface for enterprise-rag-platform."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from otel_setup import tracer
app=FastAPI(title="enterprise-rag-platform",version="1.0.0")
class RetrievalRequest(BaseModel):
 query: str
 payload: dict[str,Any]={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/retrieval")
def handle(req:RetrievalRequest):
 with tracer.start_as_current_span("retrieval") as span:
  span.set_attribute("request.key",getattr(req,"query"))
  return {"status":"accepted","query":getattr(req,"query")}
