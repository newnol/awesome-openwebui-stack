# Awesome Open WebUI Tools

A **community-facing showcase**: finished **stacks**, **tools**, **functions**, and **pipes** worth knowing about for [Open WebUI](https://github.com/open-webui/open-webui). Each listing should point to something **usable today** (repo, release, or official/community post)—this is **not** a tutorial repo for building new tools.

1. **What’s worth trying?** Curated entries with clear purpose and a stable link.
2. **What’s it for?** Browse by **categories** (goal) or **catalog** (artifact type).
3. **Where’s the implementation?** Outbound links only; source code lives in upstream repos.

**Bar for inclusion:** the stack or tool/function/pipe is **complete enough to recommend** (or honestly labeled **Beta** / **Unmaintained** with context). For **how to author** tools, pipes, or filters, use **[Open WebUI documentation](https://docs.openwebui.com/)** and upstream source—not this repository.

---

## Who this is for

- People picking proven patterns (stacks) or add-ons for Open WebUI.
- Authors who want to **promote** something already shipped.
- Readers comparing options—not step-by-step “create your first tool” guides.

---

## Selection criteria

Prefer **public source**, **clear license**, and **accurate status**. See [docs/review-criteria.md](docs/review-criteria.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Quick navigation

| Browse by | Description |
|-----------|-------------|
| [catalog/tools.md](catalog/tools.md) | Python tools (callable from the UI) |
| [catalog/functions.md](catalog/functions.md) | Functions (filters, actions, etc.) |
| [catalog/pipes.md](catalog/pipes.md) | Pipes (model routing, custom pipelines) |
| [catalog/stacks.md](catalog/stacks.md) | Reference stacks + template |
| [catalog/integrations.md](catalog/integrations.md) | External services and connection patterns |
| [catalog/learning-resources.md](catalog/learning-resources.md) | Official docs and external learning links |

**By goal:**

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

**Stacks:** [stacks/openwebui-stack/](stacks/openwebui-stack/) — index [stacks/README.md](stacks/README.md).

---

## Featured stack

- **[Open WebUI stack](stacks/openwebui-stack/)** — Example compose-oriented layout (LiteLLM, search, RAG outline). Each stack README includes an **author GitHub** link.

---

## Implementations we link to

Maintainer examples live in **[openwebui-extension](https://github.com/newnol/openwebui-extension)** — listed in [catalog/tools.md](catalog/tools.md) and [catalog/pipes.md](catalog/pipes.md).

---

## Contributing

Add **finished** listings only. See [CONTRIBUTING.md](CONTRIBUTING.md), [docs/submission-guidelines.md](docs/submission-guidelines.md), [docs/review-criteria.md](docs/review-criteria.md), [docs/category-guide.md](docs/category-guide.md), [docs/faq.md](docs/faq.md). Issues: [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/).

---

## Scope

| This repo | Elsewhere |
|-----------|-----------|
| Short blurbs + links to **shipped** work | How-to author extensions → **[docs.openwebui.com](https://docs.openwebui.com/)** |
| Optional small `docker-compose` next to a stack README | Large production-only infra repos |
| Curation & discovery | Full tool source trees (own GitHub repo) |

---

## License

MIT — see [LICENSE](LICENSE).
