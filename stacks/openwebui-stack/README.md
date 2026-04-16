# Open WebUI stack (Claude-style cloud + LiteLLM)

## Author

| Field | Link |
|-------|------|
| **GitHub** | [https://github.com/newnol](https://github.com/newnol) |

## Use case

Use this stack **if you want Claude-like coding in the cloud** through Open WebUI, **many provider API keys in one place**, and **enough visibility to track cost** (via LiteLLM and provider dashboards). You deploy with **Docker Compose**, wire **web search** and **RAG**, and keep execution behind **Open Terminal** (or equivalent) for running code safely.

## Comparison with ChatGPT

| Topic | This stack | ChatGPT (consumer cloud) |
|-------|------------|---------------------------|
| Hosting | Your VM / VPS; you control network and regions | OpenAI-hosted only |
| Models | Any provider LiteLLM can proxy (Anthropic, OpenAI, OpenRouter, …) | OpenAI models in the product |
| API keys | Centralized in **LiteLLM**; optional budgets / routing per key | Not applicable (subscription billing) |
| Tools & RAG | You choose Open WebUI tools, functions, OCR, embeddings, rerank | Fixed product surface |
| Compliance | You define retention, egress, and regions | Vendor terms only |

## Host / hardware configuration

Document the machine (or VM) that runs this stack so others can size and reproduce it.

| Field | Example | Your values |
|-------|---------|---------------|
| **CPU** | 4 vCPU | |
| **RAM** | 16 GB (Open WebUI + LiteLLM + light RAG workers) | |
| **Disk** | 80 GB SSD (SQLite + uploads + vector index) | |
| **GPU** | None (API-only models) or note if you run local embed/rerank | |
| **OS** | Ubuntu 22.04 LTS | |
| **Network** | Public IPv4 + TLS termination (reverse proxy) | |

> **Note:** If **Mistral OCR**, **local embeddings**, or **rerank** run on-box, increase RAM/CPU or add a GPU line here. API-only RAG steps can stay small.

## Deployment (Docker Compose)

Commit a **`docker-compose.yml`** in this folder (and **`.env.example`** without secrets) when you want a reproducible deploy. The compose file should include at least:

1. **Open WebUI** — Chat UI, tools, functions; **database: SQLite** (simple single-node) or switch to Postgres if you need HA.
2. **LiteLLM** — OpenAI-compatible **gateway** for multiple providers; **store and route keys**, optional **spend tracking** per model or key.
3. **Open Terminal** (or your chosen **code execution** service) — Lets the assistant run commands/snippets in a **controlled** environment; **never** expose an unrestricted host shell.

Optional: reverse proxy (Caddy / Traefik) for HTTPS, workers for heavy RAG ingestion.

## List of tools

Fill in what you actually enable in Open WebUI (names + links to source or community posts):

| Tool | Purpose | Source |
|------|---------|--------|
| *e.g. web search tool* | Grounding | *link* |
| *e.g. file / repo tools* | Context | *link* |
| *(add rows)* | | |

## List of functions / pipes

| Kind | Name | Purpose | Source |
|------|------|---------|--------|
| Pipe / Function | *(add rows)* | | |

## Web search provider

- **Provider:** [Tavily](https://tavily.com/) (or another API Open WebUI supports).
- **Plan:** Free tier often includes on the order of **~1,000 searches/month**—confirm current limits on Tavily’s site and record the tier you rely on in your runbook.

## RAG

| Stage | Choice (this stack) | Notes |
|-------|------------------------|--------|
| **OCR / ingest** | Mistral OCR (or compatible pipeline) | Tune for your file types |
| **Embeddings** | OpenAI-compatible **embedding** API (or another “open” embedding endpoint you configure) | Match dims to your vector store |
| **Rerank** | Dedicated **rerank** model or API | Improves top-k quality before the model reads chunks |

## Cost and keys

- **LiteLLM:** Primary place to register provider keys and inspect usage where supported.
- **Open WebUI:** Admin roles for who can install tools that call the network.

## See also

- [Template for new stacks](../template-full-stack/README.md)
- [Stack format](../../docs/stack-format.md)
