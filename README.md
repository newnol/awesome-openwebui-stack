# Awesome Open WebUI Stack

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Checks](https://github.com/newnol/awesome-openwebui-stack/actions/workflows/checks.yml/badge.svg)](https://github.com/newnol/awesome-openwebui-stack/actions/workflows/checks.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**English** | [Tiếng Việt](README.vi.md)

Find Open WebUI tools, functions, pipes, integrations and reference stacks **by what you want to do**. Compare prerequisites, inspect the evidence, and follow the original project's setup instructions.

**[Open the catalog explorer](https://newnol.github.io/awesome-openwebui-stack/)** | **[Start here](START-HERE.md)** | **[Browse on GitHub](catalog/README.md)** | **[Suggest an entry](CONTRIBUTING.md)**

## Find your starting point

| Your goal | Start with | What to check |
| --- | --- | --- |
| Analyze CSV or Excel | [SheetProof](catalog/tools.md#sheetproof) + [Router](catalog/functions.md#sheetproof-router) | Tool-calling model, Python dependencies, file privacy |
| Use local models | [Ollama](catalog/integrations.md#ollama) | Model resources and server connectivity |
| Connect model providers | [LiteLLM](catalog/integrations.md#litellm) | Provider keys, proxy permissions, data handling |
| Search the web | [SearXNG](catalog/integrations.md#searxng) | JSON output and access to upstream search engines |
| Run code and work with files | [Open Terminal](catalog/integrations.md#open-terminal) | Isolation, API key, filesystem and network permissions |
| Explore a multi-service setup | [Reference stack](stacks/openwebui-stack/README.md) | Example only; review secrets and exposed ports |

## Explore without guesswork

The website provides text search, filters for use case/type/evidence, a three-entry comparison, shareable filter URLs, mobile layouts and a light/dark theme. There is no sign-in, installation service, analytics tracker or API token requirement for browsing. The explorer loads only local static assets; the separate Docsify guide viewer retains its existing CDN dependencies.

Every listing states its requirements, compatibility limitations, safety notes, source-review date and evidence link. **Source documented is not the same as tested, audited, maintained or endorsed.** Five legacy listings currently have no implementation at their linked source and are hidden from the explorer by default, but retained with explicit warnings in Markdown.

## Browse the collection

| By artifact | By goal |
| --- | --- |
| [Tools](catalog/tools.md) | [Coding](categories/coding.md), [Research](categories/research.md) |
| [Functions](catalog/functions.md) | [Productivity](categories/productivity.md), [Security](categories/security.md) |
| [Pipes](catalog/pipes.md) | [Automation](categories/automation.md), [Multi-agent](categories/multi-agent.md) |
| [Stacks](catalog/stacks.md) | [Self-hosting](categories/self-hosting.md) |
| [Integrations](catalog/integrations.md) | [RAG](categories/rag.md) |
| [Learning resources](catalog/learning-resources.md) | [All entries](catalog/README.md) |

## Contribute once, publish everywhere

Listing data lives in [`data/catalog.json`](data/catalog.json). A [JSON Schema](data/catalog.schema.json) and automated checks protect the format. The explorer reads this data directly; a generator produces the artifact catalogs and category pages.

```bash
node scripts/catalog.mjs
node --test tests/catalog.test.mjs
node scripts/catalog.mjs --check
```

No Node package installation is required for these commands (Node 22+). See [contributing](CONTRIBUTING.md), [submission guidelines](docs/submission-guidelines.md), [review criteria](docs/review-criteria.md), and the [maintenance guide](docs/catalog-maintenance.md).

## Preview locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000` for the explorer and `http://localhost:8000/guide.html` for the guides. Do not open `index.html` with `file://`; loading catalog JSON requires an HTTP server. Existing `/#/catalog/...` bookmarks redirect to the guide viewer.

## Scope and license

This is a curated community directory, not an app store, security certification or tutorial for writing extensions. Source code belongs in upstream repositories; small reference Compose examples can live beside stack write-ups. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

The directory is MIT licensed; each linked project, model and hosted service has its own license or terms. This project is not affiliated with Open WebUI.
