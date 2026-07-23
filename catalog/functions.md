# Functions

Open WebUI **functions** include filters, actions, and other server-side hooks (see [functions documentation](https://docs.openwebui.com/features/extensibility/plugin/functions/)).

This file lists **finished** function packages (installable from their **Source** links). To **write** new functions, use [Open WebUI functions documentation](https://docs.openwebui.com/features/extensibility/plugin/functions/)—not this repo.

---

## Catalog entries (additions welcome)

Use the format in [submission guidelines](../docs/submission-guidelines.md).

### Example placeholder

```markdown
## Function name
- **Purpose:** …
- **Best for:** …
- **Category:** …
- **Source:** …
- **Status:** …
```

Submit filters, inlet/outlet scripts, and reusable function modules here as they are verified.

---

## SheetProof Router

- **Type:** Function (filter)
- **Purpose:** Companion filter for the SheetProof tool: on a spreadsheet upload it removes the file from retrieval, enables the tool with native function calling, injects a "numbers only from the tool" contract, and audits the final answer against the tool's results.
- **Best for:** Preventing hallucinated figures in spreadsheet chats, keeping raw rows out of the model prompt.
- **Category:** Productivity, Security
- **Stack fit:** [Open WebUI stack](../stacks/openwebui-stack/)
- **Status:** Stable
- **Source:** [Almehmadi-Ai/sheetproof](https://github.com/Almehmadi-Ai/sheetproof)
- **Notes:** MIT licensed. Optional but recommended alongside the SheetProof tool. Acts only on chats that have a spreadsheet attached; all other chats pass through untouched.
