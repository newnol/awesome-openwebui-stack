# Submission guidelines

Listings here are **introductions to finished work**: a stack you run, or a tool/function/pipe others can install from your linked source. **Do not** submit tutorial-only content or stubs without a working artifact—use [Open WebUI docs](https://docs.openwebui.com/) for “how to build.”

## Entry format

Use one of these patterns so the catalog stays scannable.

### Detailed block

```markdown
## Name
- **Type:** Tool | Function | Pipe | Integration | Stack
- **Purpose:** One line.
- **Best for:** Comma-separated use cases.
- **Category:** See [category-guide.md](category-guide.md).
- **Stack fit:** Which stack docs link here, if any.
- **Status:** Stable | Beta | Experimental | Unmaintained
- **Source:** [Repository or docs](https://example.com)
- **Notes:** Optional caveats, license, or setup hints.
```

### Compact line

```markdown
### [Name](https://example.com)
- **Purpose:** …
- **Best for:** …
- **Stack fit:** …
- **Status:** Stable
```

## Required fields

- **Purpose** and **Best for** (or equivalent).
- **Source** link unless the item is fully documented inside this repo (then use a relative path).
- **Status** when you know maintenance reality; otherwise write **Unknown** and say why.

## Quality bar

- Prefer primary sources (author repo, official docs).
- No affiliate-only links as the sole source.
- If you duplicate an upstream README, add one sentence on why Open WebUI users should care.

## Where entries live

| Kind | Primary file |
|------|----------------|
| Tool | [catalog/tools.md](../catalog/tools.md) |
| Function | [catalog/functions.md](../catalog/functions.md) |
| Pipe | [catalog/pipes.md](../catalog/pipes.md) |
| **Stack** (showcase README) | New folder **`stacks/<name>/`** with **`README.md`** including **Author (GitHub)** (copy [template-full-stack](../stacks/template-full-stack/README.md); optional `docker-compose.yml`) per [stack-format.md](stack-format.md) + row in [catalog/stacks.md](../catalog/stacks.md) |
| Integration | [catalog/integrations.md](../catalog/integrations.md) |
| Learning | [catalog/learning-resources.md](../catalog/learning-resources.md) |

Also add cross-links from relevant [categories/](../categories/) pages when it helps readers who browse by goal.
