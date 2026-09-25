import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    document_id: str
    text: str
    index: int


def chunk_document(document_id: str, text: str, size: int = 512) -> list[Chunk]:
    if not document_id.strip() or not text.strip() or size < 32:
        raise ValueError("invalid document")
    words = text.split()
    return [
        Chunk(document_id, " ".join(words[i : i + size]), i // size)
        for i in range(0, len(words), size)
    ]


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
