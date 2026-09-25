from rag_domain import *
def test_chunk_and_retrieve():
 c=chunk_document("d","alpha beta gamma alpha",2); assert len(c)==2
 assert lexical_retrieve("alpha",c)[0][0].document_id=="d"