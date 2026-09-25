from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from rag_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"enterprise-rag-platform"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="enterprise-rag-platform",version="1.0.0");tracer=trace.get_tracer("enterprise-rag-platform")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/retrieve")
def handle(r:Request):
 with tracer.start_as_current_span("enterprise-rag-platform.domain"):
  try: chunks=chunk_document(r.key,r.payload.get("text","")); hits=lexical_retrieve(r.payload.get("query",r.key),chunks); return {"status":"ok","results":[{"text":c.text,"score":s,"document_id":c.document_id,"chunk":c.index} for c,s in hits]}
  except (ValueError,KeyError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
