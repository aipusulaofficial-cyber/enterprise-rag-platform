"""Versioned RAG retrieval contract."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalEvidence:
    query_id: str
    index_version: str
    document_ids: tuple[str, ...]
    citation_valid: bool


def valid(evidence: RetrievalEvidence) -> bool:
    return bool(
        evidence.query_id
        and evidence.index_version
        and evidence.document_ids
        and evidence.citation_valid
    )
