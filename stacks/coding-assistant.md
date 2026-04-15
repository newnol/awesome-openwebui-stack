# Stack: Coding assistant

## Goal

Support **read, write, review, and explain code** from chat, with optional **diagrams** and **repository context** (via your own RAG or IDE integration patterns).

## Typical use cases

- Refactors and reviews with citations to files or snippets
- Generating architecture diagrams for documentation
- Pair-programming style Q&A

## Recommended components (pattern)

| Layer | Role |
|-------|------|
| Model | Capable coding model (local or API—your policy) |
| Tools | File-aware tools if you expose a repo; diagram tool for visuals |
| Functions | Filters for style or policy if you enforce org rules |
| Knowledge | Optional RAG over internal docs ([RAG workbench](rag-workbench.md)) |

## Maintainer examples

- **Diagram Generator** and **Auto Tool Filter** — see [catalog/tools.md](../catalog/tools.md); source in [openwebui-extension](https://github.com/newnol/openwebui-extension).

## Trade-offs

- **Large tool menus** confuse models—prefer filtering or a short allowlist.
- **Long contexts** cost more; structure prompts and retrieved chunks deliberately.

## Where to find code or deploy guidance

- Tool sources: [catalog/tools.md](../catalog/tools.md)
- Official feature overview: [Open WebUI tools](https://docs.openwebui.com/features/plugin/tools/)
