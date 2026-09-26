from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import (
    PrincipalObservabilityMiddleware,
    configure_observability,
    get_logger,
)
from rag_domain import chunk_document, lexical_retrieve

configure_observability()
logger = get_logger(__name__)

app = FastAPI(title="enterprise-rag-platform", version="1.0.0")
app.add_middleware(PrincipalObservabilityMiddleware)
tracer = trace.get_tracer("enterprise-rag-platform")


class RetrievePayload(BaseModel):
    text: str = Field(default="", max_length=100_000)
    query: str | None = Field(default=None, min_length=1, max_length=2_000)


class RetrieveRequest(BaseModel):
    key: str = Field(min_length=1, max_length=128)
    payload: RetrievePayload = Field(default_factory=RetrievePayload)


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/retrieve")
def handle(request: RetrieveRequest):
    with tracer.start_as_current_span("rag.retrieve") as span:
        span.set_attribute("rag.document_id", request.key)
        try:
            text = request.payload.text
            query = request.payload.query or request.key
            chunks = chunk_document(request.key, text)
            hits = lexical_retrieve(query, chunks)
            logger.info(
                "rag_retrieval document_id=%s query_terms=%d hits=%d",
                request.key,
                len(query.split()),
                len(hits),
            )
            return {
                "status": "ok",
                "results": [
                    {
                        "text": chunk.text,
                        "score": score,
                        "document_id": chunk.document_id,
                        "chunk": chunk.index,
                    }
                    for chunk, score in hits
                ],
            }
        except (ValueError, KeyError) as exc:
            logger.warning(
                "rag_request_rejected document_id=%s reason=%s",
                request.key,
                exc,
            )
            raise HTTPException(status_code=400, detail=str(exc)) from exc
