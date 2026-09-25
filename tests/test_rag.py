import pytest

from rag_platform import Chunk, Document, RetrievalThresholdError, Retriever, chunk_document


def test_chunk_overlap_and_identity():
    c = chunk_document(Document("d", "one two three four five six", "s"), 3, 1)
    assert c[0].id == "d:0" and c[1].text == "three four five"


def test_retrieval_returns_citations():
    d = Document("d", "security controls and retrieval quality", "s")
    r = Retriever(chunk_document(d, 20, 0), 0.2)
    h = r.retrieve("security retrieval")
    assert h and h[0].source == "s"


def test_empty_query_fails():
    with pytest.raises(ValueError):
        Retriever([]).retrieve(" ")


def test_threshold_failure_is_explicit():
    with pytest.raises(RetrievalThresholdError):
        Retriever([Chunk("x", "d", "hello", "s")], 0.9).retrieve("security")
