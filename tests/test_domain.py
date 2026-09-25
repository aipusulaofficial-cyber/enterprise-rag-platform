from rag_domain import chunk_document, lexical_retrieve


def test_chunk_and_retrieve():
    text = "alpha beta gamma alpha " * 20
    chunks = chunk_document("d", text, 32)
    assert len(chunks) == 3
    assert lexical_retrieve("alpha", chunks)[0][0].document_id == "d"
