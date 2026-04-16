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

**[docker-compose.yml](docker-compose.yml)** runs **Open WebUI**, **Open Terminal**, **LiteLLM** (proxy), and **Postgres** for LiteLLM’s DB. Monitoring stack (**Prometheus**, **Grafana**, **Dozzle**, **Loki**, **Promtail**) is omitted on purpose.

**Prerequisites**

1. Docker network **`ai-network`** must exist (`external: true`). Create once: `docker network create ai-network`
2. **`config.yaml`** next to the compose file (start from [config.yaml.example](config.yaml.example)).
3. **`.env`** — copy [`.env.example`](.env.example) to `.env` and set secrets. Compose uses it for **`${OPEN_TERMINAL_API_KEY}`**, **`${POSTGRES_PASSWORD}`**, and **`litellm`’s `DATABASE_URL`**. **`env_file: .env`** is set on **open-webui** and **litellm** so optional Open WebUI / provider variables in the same file are passed into those containers (see comments in `.env.example`).

**Run**

`docker compose up -d`

Set **`OPEN_TERMINAL_API_KEY`** for Open Terminal. Point Open WebUI at LiteLLM’s OpenAI-compatible URL (e.g. `http://litellm:4000` from other containers, or `http://<host>:4000` from the host).

**Postgres volume:** compose uses a normal named volume `postgres_data`. To **reuse** an existing volume instead, replace the `postgres_data:` entry under `volumes:` with `external: true` and `name: <your_volume_name>`.

**Ports:** Postgres is published on **5432** — restrict with firewall or remove the `ports:` mapping on `db` if only LiteLLM needs DB access on the Docker network.

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
