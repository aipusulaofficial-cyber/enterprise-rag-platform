import time

from fastapi import FastAPI, HTTPException
from fastapi import Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field

from observability import PrincipalObservabilityMiddleware, configure_observability, get_logger
from rag_domain import InMemoryVectorStore, ScoreReranker, chunk_document
from runtime_evidence import request_id_from_headers, runtime_evidence
configure_observability()
logger = get_logger(__name__)
app = FastAPI(title="enterprise-rag-platform", version="1.1.0")
app.add_middleware(PrincipalObservabilityMiddleware)
tracer = trace.get_tracer("enterprise-rag-platform")
