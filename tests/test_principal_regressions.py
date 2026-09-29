import pytest

from rag_platform import Document, Retriever, chunk_document


def test_negative_overlap_rejected():
    with pytest.raises(ValueError):
        chunk_document(Document("id", "one two", "source"), size=2, overlap=-1)


def test_nonpositive_retrieval_limit_rejected():
    retriever = Retriever(chunk_document(Document("id", "one two three", "source")))
    with pytest.raises(ValueError):
        retriever.retrieve("one", k=0)
