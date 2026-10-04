import pytest

from rag_platform import Document, Retriever, chunk_document


def test_rejects_negative_overlap():
    with pytest.raises(ValueError):
        chunk_document(Document("d", "one two three", "source"), size=3, overlap=-1)


def test_avoids_overlap_only_trailing_chunks():
    doc = Document("d", " ".join(f"w{i}" for i in range(10)), "source")
    chunks = chunk_document(doc, size=6, overlap=2)
    assert len(chunks) == 2
    assert len(chunks[0].text.split()) == 6
    assert len(chunks[1].text.split()) == 6


@pytest.mark.parametrize("k", [0, -1, "5", True])
def test_retriever_rejects_invalid_k(k):
    chunks = chunk_document(Document("d", "grounded evidence", "source"))
    with pytest.raises(ValueError):
        Retriever(chunks).retrieve("grounded", k=k)
