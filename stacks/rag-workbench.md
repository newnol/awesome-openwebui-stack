# Stack: RAG workbench

## Goal

A practical pipeline from **documents** to **grounded answers** in chat: ingest, chunk, embed, retrieve, and generate with citations where possible.

## Typical use cases

- Internal handbook Q&A
- Developer docs search
- Regulated environments with audit expectations (design-dependent)

## Recommended components (pattern)

| Stage | Considerations |
|-------|------------------|
| Ingest | Formats (PDF, HTML, markdown), deduplication, access control |
| Chunking | Size, overlap, structure-aware splits for technical docs |
| Embeddings | Model choice, dimension, refresh on document change |
| Retrieval | Hybrid search (keyword + vector) when quality matters |
| Generation | Prompts that require citing retrieved chunks |

## Open WebUI touchpoints

- Use Open WebUI knowledge features per [official documentation](https://docs.openwebui.com/).
- External vector DBs belong in [catalog/integrations.md](../catalog/integrations.md) with connection notes.

## Trade-offs

- **Freshness:** stale embeddings produce confident wrong answers—plan reindexing.
- **Privacy:** document location and embedding storage must match policy.

## Where to find code or deploy guidance

- [categories/rag.md](../categories/rag.md)
- Developer references in [docs/README.md](../docs/README.md) (embeddings helpers for custom functions)
