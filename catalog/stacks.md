# Stacks

A **stack** is a **showcase** write-up for a **finished** setup you recommend: use case, **author (GitHub)**, **host hardware** if relevant, services/tools, and outbound links. Format: **[docs/stack-format.md](../docs/stack-format.md)**.

| Stack | Goal | Author (GitHub) | Doc |
|-------|------|-----------------|-----|
| Open WebUI (cloud coding, LiteLLM, Tavily, RAG) | Claude-style cloud, keys in one place, cost tracking | [@newnol](https://github.com/newnol) | [openwebui-stack/](../stacks/openwebui-stack/) |

**Template** for a new stack folder: [template-full-stack/README.md](../stacks/template-full-stack/README.md).

---

## How to contribute

1. Copy [stacks/template-full-stack/README.md](../stacks/template-full-stack/README.md) to `stacks/<your-name>/README.md`.
2. Fill the **Author** section with a GitHub user or org URL.
3. Add a row to the table above (or open a PR for maintainers to add it).
4. Optional: commit `docker-compose.yml` and `.env.example` next to `README.md` (no secrets).

See [submission guidelines](../docs/submission-guidelines.md).
