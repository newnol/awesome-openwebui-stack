# Awesome Open WebUI Tools

A curated, English-language index for discovering **tools**, **functions**, **pipes**, and **stack ideas** for [Open WebUI](https://github.com/open-webui/open-webui). It answers three questions:

1. **What is worth knowing about?** Notable tools, functions, pipes, integrations, and learning material.
2. **What is it for?** Use-case-oriented browsing via **categories** and **stacks** (composed setups for a goal).
3. **Where is the code or deployment story?** Each entry links to a repository, docs, or an upstream project (this repo does not ship tool or pipe source code).

This repository is intentionally **catalog-first**: it is not a lab image, not a production deploy repo, and not a place for large application codebases. See [Scope and boundaries](#scope-and-boundaries).

---

## Who this is for

- People choosing components for Open WebUI (chat, RAG, coding, automation, self-hosting).
- Contributors who want a clear format for submissions and reviews.
- Teams comparing **stacks** (combinations of tools, models, and infra patterns) for a specific goal.

---

## Selection criteria (high level)

Entries should be **useful**, **maintained or clearly labeled**, and **properly attributed**. We prefer items with public source or official docs. See [docs/review-criteria.md](docs/review-criteria.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Quick navigation

| Browse by | Description |
|-----------|-------------|
| [catalog/tools.md](catalog/tools.md) | Python tools (callable from the UI) |
| [catalog/functions.md](catalog/functions.md) | Functions (filters, actions, etc.) |
| [catalog/pipes.md](catalog/pipes.md) | Pipes (model routing, custom pipelines) |
| [catalog/stacks.md](catalog/stacks.md) | Stack ideas and references (composed setups) |
| [catalog/integrations.md](catalog/integrations.md) | External services and connection patterns |
| [catalog/learning-resources.md](catalog/learning-resources.md) | Docs, tutorials, official references |

**By goal (not by component type):**

| Category | File |
|----------|------|
| Coding | [categories/coding.md](categories/coding.md) |
| Research | [categories/research.md](categories/research.md) |
| RAG | [categories/rag.md](categories/rag.md) |
| Automation | [categories/automation.md](categories/automation.md) |
| Productivity | [categories/productivity.md](categories/productivity.md) |
| Multi-agent | [categories/multi-agent.md](categories/multi-agent.md) |
| Self-hosting | [categories/self-hosting.md](categories/self-hosting.md) |
| Security | [categories/security.md](categories/security.md) |

**Opinionated recipes:**

| Stack | File |
|-------|------|
| Low-cost local | [stacks/low-cost-local.md](stacks/low-cost-local.md) |
| Coding assistant | [stacks/coding-assistant.md](stacks/coding-assistant.md) |
| Research agent | [stacks/research-agent.md](stacks/research-agent.md) |
| RAG workbench | [stacks/rag-workbench.md](stacks/rag-workbench.md) |
| Privacy-first | [stacks/privacy-first.md](stacks/privacy-first.md) |

**Community-inspired (simple):** [Multi-model tools](stacks/community-multi-model-tools.md) · [Coding + debug](stacks/community-coding-debug.md) · [n8n + WebDAV](stacks/community-automation-n8n.md) · [Claude stack](stacks/community-claude-providers.md) · [Infomaniak](stacks/community-eu-infomaniak.md) · [PDF helper](stacks/community-document-assistant.md) — see [catalog/stacks.md](catalog/stacks.md).

---

## Featured stacks (start here)

- **[Coding assistant](stacks/coding-assistant.md)** — IDE-like workflows inside chat.
- **[Research agent](stacks/research-agent.md)** — retrieval, citations, and verification-oriented setups.
- **[RAG workbench](stacks/rag-workbench.md)** — documents, embeddings, and chat over your data.
- **[Low-cost local](stacks/low-cost-local.md)** — small hardware, local models, pragmatic trade-offs.
- **[Privacy-first](stacks/privacy-first.md)** — data boundaries and deployment posture.

---

## Author implementations (separate repo)

Custom tools and pipes by the maintainer live in **[openwebui-extension](https://github.com/newnol/openwebui-extension)**. This catalog lists them with links there—see [catalog/tools.md](catalog/tools.md) and [catalog/pipes.md](catalog/pipes.md). For Open WebUI internals used when writing functions, see [docs/README.md](docs/README.md).

---

## Contributing

- [CONTRIBUTING.md](CONTRIBUTING.md) — how to propose additions.
- [docs/submission-guidelines.md](docs/submission-guidelines.md) — entry format and quality bar.
- [docs/review-criteria.md](docs/review-criteria.md) — what maintainers check.
- [docs/category-guide.md](docs/category-guide.md) — choosing categories and stacks.
- [docs/faq.md](docs/faq.md) — common questions.

Use GitHub Issues from [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) for structured submissions.

---

## Scope and boundaries

| In this repo | Not in this repo (put elsewhere) |
|--------------|----------------------------------|
| Curated lists, stack write-ups, links | Full production `docker-compose` or fleet configs as the main artifact |
| Short docs and criteria | Heavy CI that runs a full Open WebUI farm |
| Pointers to code | Large tool/function codebases (prefer their own repos) |

A practical split: **this repo** = discovery and curation; a separate **lab** repo = templates and experiments; a separate **stack** repo = deployment and infra.

---

## License

This catalog is licensed under the MIT License — see [LICENSE](LICENSE).
