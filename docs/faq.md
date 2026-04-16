# FAQ

## Is this repo a tutorial for building tools?

**No.** It is a **showcase**: short blurbs and links to **finished** stacks, tools, functions, and pipes. To learn how to write extensions, use [Open WebUI documentation](https://docs.openwebui.com/) and the linked upstream repositories.

## What is the difference between catalog and categories?

- **Catalog** (`catalog/`) groups by **artifact type**: tools, functions, pipes, etc.
- **Categories** (`categories/`) groups by **goal**: coding, RAG, research, and so on.

Use both: some readers know they need a “tool”; others only know they want “better RAG.”

## What is a “stack” here?

A **reference write-up** under `stacks/<name>/README.md`—see [stacks/README.md](../stacks/README.md) and [catalog/stacks.md](../catalog/stacks.md). Each stack lists an **author GitHub** link. Example: [openwebui-stack](../stacks/openwebui-stack/). New stacks: copy [template-full-stack/README.md](../stacks/template-full-stack/README.md); details in [stack-format.md](stack-format.md).

## Does this repo ship production deployments?

Primarily **curation**: prose and optional small **`docker-compose.yml`** / **`.env.example`** next to a stack `README.md` when they help reproducibility. Large or secret-heavy infra should stay in a **separate** repository; link it from the stack doc.

## Can I submit my project?

Yes. Read [submission-guidelines.md](submission-guidelines.md) and open an issue or PR. We need a clear purpose, Open WebUI relevance, and a stable link.

## Where is official Open WebUI documentation?

Start with [Open WebUI documentation](https://docs.openwebui.com/). This catalog is independent and may link there frequently.

## What about older bilingual notes?

The **catalog** (README, `catalog/`, `categories/`, `stacks/`, contributor `docs/`) is **English-first**. Deep technical authoring for tools is **out of scope** here—see [Open WebUI documentation](https://docs.openwebui.com/).
