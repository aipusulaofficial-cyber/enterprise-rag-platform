"""Enterprise RAG domain core: deterministic retrieval contracts with citations."""

from dataclasses import dataclass
import re, sys


@dataclass(frozen=True)
class Document:
    id: str
    text: str
    source: str


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    text: str
    source: str


@dataclass(frozen=True)
class Citation:
    chunk_id: str
    source: str
    score: float


class RAGError(Exception):
    pass


class RetrievalThresholdError(RAGError):
    pass


def chunk_document(doc: Document, size: int = 120, overlap: int = 20) -> list[Chunk]:
    if size <= overlap or size <= 0:
        raise ValueError("size must be > overlap >= 0")
    words = doc.text.split()
    out = []
    step = size - overlap
    for i in range(0, len(words), step):
        text = " ".join(words[i : i + size])
        if not text:
            break
        out.append(Chunk(f"{doc.id}:{i}", doc.id, text, doc.source))
    return out


def lexical_score(query: str, text: str) -> float:
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    t = re.findall(r"[a-z0-9]+", text.lower())
    return len(q & set(t)) / max(len(q), 1)


class Retriever:
    def __init__(self, chunks: list[Chunk], threshold: float = 0.1):
        self.chunks, self.threshold = chunks, threshold

    def retrieve(self, query: str, k: int = 5) -> list[Citation]:
        if not query.strip():
            raise ValueError("query is required")
        scored = sorted(
            ((lexical_score(query, c.text), c) for c in self.chunks),
            key=lambda x: (-x[0], x[1].id),
        )
        hits = [Citation(c.id, c.source, s) for s, c in scored if s >= self.threshold][
            :k
        ]
        if not hits:
            raise RetrievalThresholdError("no grounded chunks met threshold")
        return hits


def main():
    q = " ".join(sys.argv[1:]) or "architecture"
    docs = [
        Document(
            "demo",
            "Production RAG systems require retrieval, grounding, citations and observability.",
            "demo://document",
        )
    ]
    r = Retriever(chunk_document(docs[0], 20, 5))
    for x in r.retrieve(q):
        print(x)


if __name__ == "__main__":
    main()
