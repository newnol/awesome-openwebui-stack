# Stack: Low-cost local

## Goal

Run a **useful** Open WebUI assistant on **modest hardware** (small GPU, CPU-only, or a single home server) without chasing the largest frontier models.

## Typical use cases

- Private chat for a household or small team
- Offline-first experimentation
- Cost control vs. cloud APIs

## Recommended components (pattern)

| Layer | Options | Trade-offs |
|-------|---------|------------|
| Model | Small instruct models via Ollama or similar | Lower capability; faster iteration |
| Routing | Keyword or rule-based pipe (e.g. [Auto Router Model](https://github.com/newnol/openwebui-extension)) | Simple; not semantic routing |
| Tools | Few, high-signal tools only | Less confusion; less API spend |
| RAG | Small corpora, local embeddings when possible | RAM/CPU bound; tune chunk size |

## Trade-offs

- **Latency vs. quality:** smaller models respond faster but may need tighter prompts.
- **RAM:** RAG + model together can exceed consumer limits—reduce context or corpus size.
- **Maintenance:** local stacks need update discipline (Open WebUI, models, OS).

## Where to find code or deploy guidance

- [Open WebUI docs](https://docs.openwebui.com/) — installation and configuration.
- Example router pipe: [catalog/pipes.md](../catalog/pipes.md) → [openwebui-extension](https://github.com/newnol/openwebui-extension).
- **Deploy artifacts** (compose, systemd, k8s): keep in a dedicated infra repository and link from issues or PRs here.
