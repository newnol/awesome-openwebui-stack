# Open WebUI stack (Claude-style cloud + LiteLLM)

## Author

| Field | Link |
|-------|------|
| **GitHub** | [https://github.com/newnol](https://github.com/newnol) |

## Quick start (run Open WebUI in a few minutes)

> **Reference example, not production-ready.** Proposed release candidates (reviewed 2026-11-12): Open WebUI `v0.13.3`, LiteLLM `v1.109.1`, Open Terminal `0.17.7`. This combination has **not** been deployment-tested. Production operators should additionally verify image signatures/digests, test the stack and take backups before upgrades.

Do everything **from this folder** (where `docker-compose.yml` lives). Get this folder with a **full clone**, a **sparse clone**, **`svn export`**, or a **folder ZIP** (see step **0**), then **one copy step** for the example files, edit two files, and start Docker.

### What you need installed

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose v2](https://docs.docker.com/compose/install/) (`docker compose` command).

### 0) Get this folder (`git clone`)

```bash
git clone https://github.com/newnol/awesome-openwebui-stack.git
cd awesome-openwebui-stack/stacks/openwebui-stack
```

The directory after `git clone` matches the repository name on GitHub (here: `awesome-openwebui-stack`). If you use a **fork** or GitHub shows a **renamed** default repo, `cd` into that clone directory, then into `stacks/openwebui-stack/`.

Optional shallow clone (smaller download):

```bash
git clone --depth 1 https://github.com/newnol/awesome-openwebui-stack.git
cd awesome-openwebui-stack/stacks/openwebui-stack
```

#### Get only `stacks/openwebui-stack` (no full working tree)

If you do **not** want every other file from the catalog checked out, use one of these:

##### A — Sparse clone (Git only downloads that path; history stays shallow)

Requires **Git 2.25+**. Default branch is **`main`** (change if your fork uses another name).

```bash
git clone --filter=blob:none --sparse https://github.com/newnol/awesome-openwebui-stack.git
cd awesome-openwebui-stack
git sparse-checkout set stacks/openwebui-stack
cd stacks/openwebui-stack
```

##### B — Export folder without Git (`svn`; no `.git`, good for “drop files on a server”)

Requires the **`svn`** CLI. GitHub exposes Subversion under `trunk` for the default branch:

```bash
svn export https://github.com/newnol/awesome-openwebui-stack/trunk/stacks/openwebui-stack openwebui-stack
cd openwebui-stack
```

##### C — Download a ZIP of just this folder (browser / helper)

Use [download-directory.github.io](https://download-directory.github.io/?url=https://github.com/newnol/awesome-openwebui-stack/tree/main/stacks/openwebui-stack) (third‑party; paste the URL if the branch is not `main`). Unzip, then `cd` into the extracted folder.

---

### 1) Copy the example files once

```bash
cp .env.example .env
cp config.yaml.example config.yaml
```

### 2) Edit `.env` (required before `docker compose up`)

Open `.env` in an editor and set at least:

| Variable | What to put |
|----------|-------------|
| `OPEN_TERMINAL_API_KEY` | A long random string (Open Terminal uses this). |
| `POSTGRES_PASSWORD` | A strong password (Postgres + LiteLLM `DATABASE_URL` use it). |
| `LITELLM_MASTER_KEY` | Strong LiteLLM admin key (`sk-...`); prefer scoped virtual keys for Open WebUI connections. |
| `WEBUI_SECRET_KEY` | A persistent Open WebUI signing secret. |

All four values are required and must be non-empty. Generate each with `openssl rand -hex 32` (prefix the LiteLLM master key with `sk-`). Do not reuse secrets. Keep `.env` untracked.

Uncomment and fill any **provider** API keys you use in `.env` (e.g. `GEMINI_API_KEY`) so LiteLLM can call those models.

### 3) Edit `config.yaml` (models for LiteLLM)

`config.yaml` starts with **header mappings only**. Add a **`model_list`** entry for each model you want (see [LiteLLM model config](https://docs.litellm.ai/docs/proxy/configs)).  
**Alternatively**, with `STORE_MODEL_IN_DB: "True"` in Compose, you can add models later in the **LiteLLM UI** at `http://localhost:4000` after the stack is up (log in with `LITELLM_MASTER_KEY`).

### 4) Create the Docker network (once per machine)

Compose expects an external network named **`ai-network`**. Create it if it does not exist:

```bash
docker network create ai-network 2>/dev/null || true
```

### 5) Start all services

```bash
docker compose config --quiet
docker compose pull
docker compose up -d
```

Wait until containers are healthy (first pull can take several minutes). All host-published ports are bound to **127.0.0.1**, while PostgreSQL is not published at all. Use an authenticated TLS reverse proxy or private tunnel for remote access; do not widen the binds without an access-control plan.

### 6) Open in the browser

| Service | URL | Notes |
|---------|-----|--------|
| **Open WebUI** | [http://localhost:3000](http://localhost:3000) | Create the first admin account on first visit. |
| **LiteLLM** | [http://localhost:4000](http://localhost:4000) | Admin / model UI; use `LITELLM_MASTER_KEY` when asked for a key. |
| **Open Terminal** | `http://localhost:18000` | Loopback-only API; connect Open WebUI using `http://open-terminal:8000`. |

### 7) Connect Open WebUI to LiteLLM (one-time in the UI)

Inside Open WebUI: **Admin panel → Settings → Connections** (wording may vary slightly by version).

- Set **OpenAI API** base URL to: `http://litellm:4000/v1`  
  (This hostname works **from the Open WebUI container** on the same Docker network.)
- Set **API key** to a scoped LiteLLM virtual key if possible. Reserve `LITELLM_MASTER_KEY` for administration.

Save, then pick an OpenAI‑compatible model in chat that matches a model you configured in LiteLLM.

### 8) Stop or update

```bash
docker compose down   # stop (named volumes persist)
docker compose config --quiet
docker compose pull && docker compose up -d   # apply updated pinned tags
```

**Upgrade warning:** Back up the `open-webui` and `postgres_data` volumes and record existing image digests before upgrading. Open WebUI 0.13.0 includes database schema migrations, so rolling back an image is *not* a database rollback. LiteLLM 1.109.x also changes fallback targets and caching: review [action-required items](https://github.com/BerriAI/litellm/releases/tag/v1.109.0) against your real `config.yaml`. Restore both images and data from backup if migration fails.

### Troubleshooting (short)

- **`network ai-network not found`** → run step 4 again.  
- **LiteLLM unhealthy** → check `config.yaml` syntax and that `LITELLM_MASTER_KEY` / DB password match `.env`.  
- **Open WebUI cannot reach LiteLLM** → base URL must be `http://litellm:4000/v1` (Docker DNS name `litellm`), not `localhost`, from inside the Open WebUI container.

---

## Security and compatibility notes

- The Compose example no longer supplies fallback credentials. Fill `POSTGRES_PASSWORD`, `OPEN_TERMINAL_API_KEY`, `LITELLM_MASTER_KEY`, and `WEBUI_SECRET_KEY` in a private `.env`.
- WebUI, LiteLLM and Open Terminal bind to loopback on the host; only trusted workloads should join the existing external `ai-network`. Restrict request paths that carry user-identity headers before enabling LiteLLM header mappings.
- Open Terminal executes commands; do not mount host Docker sockets or sensitive directories for untrusted workloads. Restrict egress and API keys.
- Release tags improve predictability over `latest`, but are **not** cryptographically immutable digest pins. PostgreSQL still tracks the `16` major line; resolve verified digests for strict reproducibility.
- Release references: [Open WebUI v0.13.3](https://github.com/open-webui/open-webui/releases/tag/v0.13.3), [Open WebUI v0.13.0 migrations/security](https://github.com/open-webui/open-webui/releases/tag/v0.13.0), [LiteLLM v1.109.1](https://github.com/BerriAI/litellm/releases/tag/v1.109.1), [Open Terminal v0.17.7](https://github.com/open-webui/open-terminal/releases/tag/v0.17.7).

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

## Compose file reference

**[docker-compose.yml](docker-compose.yml)** defines **Open WebUI**, **Open Terminal**, **LiteLLM**, and **Postgres**. A full Prometheus/Grafana/Loki monitoring bundle is **not** included here.

- **`.env` / `.env.example`** — secrets and compose substitution; see Quick start.  
- **`config.yaml` / `config.yaml.example`** — LiteLLM proxy config.  
- **Postgres volume** `postgres_data` is a normal named volume. To attach an existing volume, edit the bottom of `docker-compose.yml` (`external: true` + `name: …`).  
- **Port 5432** is exposed for Postgres — tighten firewall in production or drop the `ports:` section on `db` if only internal access is needed.

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
