import pytest

from rag_platform import Document, Retriever, chunk_document


def test_negative_overlap_rejected():
    with pytest.raises(ValueError):
        chunk_document(Document("id", "one two", "source"), size=2, overlap=-1)


def test_nonpositive_retrieval_limit_rejected():
    retriever = Retriever(chunk_document(Document("id", "one two three", "source")))
    with pytest.raises(ValueError):
        retriever.retrieve("one", k=0)


def test_multilingual_lexical_tokens_have_stable_normalization():
    from rag_platform import lexical_score

    assert lexical_score("café", "cafe engineering") == 1.0
    assert lexical_score("İSTANBUL", "istanbul systems") == 1.0


@pytest.mark.parametrize("threshold", [float("nan"), float("inf"), -0.1, 1.1])
def test_invalid_retrieval_threshold_rejected(threshold):
    with pytest.raises(ValueError):
        Retriever([], threshold=threshold)
