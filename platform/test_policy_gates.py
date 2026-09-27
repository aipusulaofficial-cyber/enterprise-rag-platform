from platform.retrieval_contract import RetrievalEvidence, valid

def test_retrieval_evidence():
    assert valid(RetrievalEvidence("q1","idx1",("doc1",),True))
    assert not valid(RetrievalEvidence("q1","idx1",(),True))
