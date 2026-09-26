import math
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Chunk:
    document_id: str
    text: str
    index: int


@dataclass(frozen=True)
class RetrievalHit:
    chunk: Chunk
    score: float


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...


class Reranker(Protocol):
    def rerank(self, query: str, hits: list[RetrievalHit]) -> list[RetrievalHit]: ...


def chunk_document(document_id: str, text: str, size: int = 512) -> list[Chunk]:
    if not document_id.strip() or not text.strip() or size < 32:
        raise ValueError("invalid document")
    words = text.split()
    return [Chunk(document_id, " ".join(words[i : i + size]), i // size) for i in range(0, len(words), size)]


def lexical_retrieve(query: str, chunks: list[Chunk], top_k: int = 5) -> list[tuple[Chunk, float]]:
    terms = set(query.lower().split())
    if not terms or top_k < 1:
        return []
    scored = []
    for chunk in chunks:
        tokens = set(chunk.text.lower().split())
        score = len(terms & tokens) / math.sqrt(max(1, len(terms) * len(tokens)))
        if score > 0:
            scored.append((chunk, score))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]


class HashEmbedder:
    """Dependency-free deterministic embedding adapter for local/reference deployments."""
    def __init__(self, dimensions: int = 256) -> None:
        if dimensions < 32:
            raise ValueError("dimensions must be >= 32")
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in text.lower().split():
            vector[hash(token) % self.dimensions] += 1.0
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]


class InMemoryVectorStore:
    """Vector-store abstraction with deterministic cosine similarity."""
    def __init__(self, embedder: Embedder | None = None) -> None:
        self.embedder = embedder or HashEmbedder()
        self._items: list[tuple[Chunk, list[float]]] = []

    def upsert(self, chunks: list[Chunk]) -> None:
        self._items.extend((chunk, self.embedder.embed(chunk.text)) for chunk in chunks)

    def search(self, query: str, top_k: int = 5) -> list[RetrievalHit]:
        if not query.strip() or top_k < 1:
            return []
        q = self.embedder.embed(query)
        hits = []
        for chunk, vector in self._items:
            score = sum(a * b for a, b in zip(q, vector))
            if score > 0:
                hits.append(RetrievalHit(chunk, score))
        return sorted(hits, key=lambda x: (-x.score, x.chunk.document_id, x.chunk.index))[:top_k]


class ScoreReranker:
    def rerank(self, query: str, hits: list[RetrievalHit]) -> list[RetrievalHit]:
        terms = set(query.lower().split())
        return sorted(
            hits,
            key=lambda h: (-len(terms & set(h.chunk.text.lower().split())), -h.score, h.chunk.index),
        )
