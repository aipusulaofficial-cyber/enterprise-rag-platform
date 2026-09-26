from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field
from observability import PrincipalObservabilityMiddleware, configure_observability, get_logger
from rag_domain import chunk_document, InMemoryVectorStore, ScoreReranker

configure_observability(); logger=get_logger(__name__)
app=FastAPI(title="enterprise-rag-platform",version="1.1.0"); app.add_middleware(PrincipalObservabilityMiddleware)
tracer=trace.get_tracer("enterprise-rag-platform")
class RetrievePayload(BaseModel):
    text:str=Field(default="",max_length=100_000); query:str|None=Field(default=None,min_length=1,max_length=2_000)
class RetrieveRequest(BaseModel):
    key:str=Field(min_length=1,max_length=128); payload:RetrievePayload=Field(default_factory=RetrievePayload)
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/retrieve")
def handle(request:RetrieveRequest):
    with tracer.start_as_current_span("rag.retrieve"):
        try:
            query=request.payload.query or request.key
            chunks=chunk_document(request.key,request.payload.text)
            store=InMemoryVectorStore(); store.upsert(chunks)
            hits=ScoreReranker().rerank(query,store.search(query,top_k=10))[:5]
            return {"status":"ok","results":[{"text":h.chunk.text,"score":h.score,"document_id":h.chunk.document_id,"chunk":h.chunk.index,"source":h.chunk.document_id} for h in hits]}
        except (ValueError,KeyError) as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
