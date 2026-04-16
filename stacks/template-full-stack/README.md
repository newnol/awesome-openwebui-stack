# Stack: {Title}

> Use this template to **describe a stack you already run or publish** for others to copy at a high level—not a from-zero tutorial. Link out for deploy artifacts and tool source.

## Author

| Field | Link |
|-------|------|
| **GitHub** | `https://github.com/{username-or-organization}` |

## Use case

{Who is this for? What do they want?}

## Comparison with {alternative}

| Topic | This stack | {ChatGPT / other} |
|-------|------------|---------------------|
| Hosting | … | … |
| Model routing | … | … |
| Cost visibility | … | … |
| Data residency | … | … |

## Host / hardware configuration

| Field | Example | Your values |
|-------|---------|---------------|
| **CPU** | e.g. 4 vCPU | |
| **RAM** | e.g. 16 GB | |
| **Disk** | e.g. SSD size for DB + uploads + indexes | |
| **GPU** | Optional: for local embed / rerank / OCR | |
| **OS** | e.g. Ubuntu LTS | |
| **Network** | e.g. TLS, reverse proxy, egress policy | |

## Deployment overview

- **Method:** Docker Compose (or describe alternative).
- **Files:** Add **`docker-compose.yml`** and **`.env.example`** in this folder (or link a companion repo).

### Docker Compose services (outline)

1. **Open WebUI** — UI + chat; **SQLite** or Postgres.
2. **LiteLLM** — Provider keys, routing, optional spend tracking.
3. **Open Terminal** (or code-execution sidecar) — Sandboxed execution for “run code” tools.

> Do not commit secrets.

## Tools (Open WebUI)

| Tool | Purpose | Source |
|------|---------|--------|
| *Name* | *One line* | *Link* |

## Functions / pipes

| Kind | Name | Purpose | Source |
|------|------|---------|--------|
| Pipe / Function | *Name* | *One line* | *Link* |

## Web search provider

- **Provider:** e.g. Tavily — note free tier limits (e.g. monthly search cap).
- **Wiring:** How it connects in Open WebUI (admin settings or tool).

## RAG

| Stage | Choice | Notes |
|-------|--------|--------|
| OCR / ingest | e.g. Mistral OCR | |
| Embeddings | e.g. OpenAI-compatible API | |
| Vector store | e.g. built-in, Qdrant, pgvector | |
| Rerank | e.g. cross-encoder or API | |

## Cost and keys

- Where keys live (LiteLLM, Open WebUI admin).
- How you track spend.

## Trade-offs

- …

## See also

- [stack-format.md](../../docs/stack-format.md)
