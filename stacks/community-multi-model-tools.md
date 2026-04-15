# Stack: Multi-model + heavy tooling

## Goal

Use **many cloud models** through one pipe and run **several tools** without everything blocking in series—typical “power user” chat with OpenRouter-style routing.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Pipe / integration | OpenRouter Integration (350+ models, multimodal, native tools) | [openwebui.com](https://openwebui.com/posts/9ac806c5-c7e3-4710-9ff3-ec900739b6db) |
| Tool | Parallel Tools | [openwebui.com](https://openwebui.com/posts/1d44cfce-d810-49b1-bbcb-52cea19c2dcf) |

## How it fits together

1. Install/configure the **OpenRouter**-style function first (admin keys, valves).
2. Add **Parallel Tools** so independent tool calls can overlap when the model requests them.
3. Keep the enabled tool list **focused**—large menus still confuse models.

## Trade-offs

- **Cost / data**: cloud APIs and uploads leave your trust boundary—review provider terms.
- **Complexity**: more moving parts than a single local model.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md); verify each project before production.
