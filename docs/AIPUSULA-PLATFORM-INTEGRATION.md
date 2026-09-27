# AIPusula Platform Integration — Production RAG

## Retrieval pipeline
`ingestion -> chunking -> embedding -> vector index -> hybrid retrieval -> reranking -> context assembly -> LLM -> citation validation -> evaluation`

A production RAG path must preserve document/version metadata and trace the retrieval decision to the final answer.

## Retrieval evidence
Measure Recall@K, Precision@K, MRR/NDCG. For generated answers measure faithfulness, context relevance, answer relevance and citation correctness.

## Contract
Every answer should expose or internally retain:
- query ID / trace ID
- dataset/index version
- retrieved document IDs
- retrieval scores
- reranker version
- prompt version
- model/version
- citation validation result
- evaluation result

## Integration points
- secure-ai-gateway: data/security policy
- agentic-engineering-platform: governed retrieval tool
- distributed-ai-inference-platform: generation
- ai-evaluation-platform: retrieval and answer quality gate
- ai-observability-platform: retrieval + generation trace
- ai-cost-optimization-platform: embedding/retrieval/generation cost

## Engineering standard
Code -> Contract -> Test -> Security -> Runtime -> Observability -> Deployment -> Evidence
