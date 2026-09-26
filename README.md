# Enterprise RAG Platform

A retrieval-augmented generation platform that separates retrieval, provider adapters, generation and operational controls into explicit boundaries.

## RAG lifecycle
```text
query -> request contract -> retrieval -> context assembly -> generation -> validated response
              |                 |             |                |
           policy          retriever       provenance       model adapter
```

## Core contracts
- Query inputs are validated before retrieval.
- Retrieval providers are replaceable adapters.
- Context assembly is distinct from model invocation.
- Dependency failures are explicit and do not become fabricated answers.
- Operational context follows the request through the pipeline.

## Reliability
External stores and model providers are isolated from domain logic. Timeouts, failure paths and health behavior are part of the production contract.

## Security
Input validation, least-privilege boundaries and security CI protect the service boundary. Sensitive provider credentials are configuration concerns, not application output.

## Evidence
[ARCHITECTURE.md](ARCHITECTURE.md) · [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md) · [ADRs](ADRs/)

This is a system for operating RAG workflows, not a prompt-only demo.