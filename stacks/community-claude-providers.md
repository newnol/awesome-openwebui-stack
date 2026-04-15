# Stack: Claude-focused providers + bridges

## Goal

Standardize on **Anthropic** models inside Open WebUI while optionally **bridging** tool formats or mixing provider APIs—useful when your org standardizes on Claude but still uses OpenAI-compatible stacks elsewhere.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Function | Anthropic API Integration (Claude 4 / 4.5 / Opus + tools) | [openwebui.com](https://openwebui.com/posts/1a167991-2684-47f6-a695-bdfc2c1f54a1) |
| Pipe / function | Claude OpenAI Tools Bridge Pipe | [openwebui.com](https://openwebui.com/posts/7e79c01f-ade8-4eed-a9c1-88971736f86b) |

## How it fits together

1. Configure **Anthropic API Integration** with org keys and model allowlist.
2. Add the **bridge** only if you need OpenAI-style tool calling interop—otherwise keep one path to reduce bugs.

## Trade-offs

- **Vendor lock-in**: Claude + Anthropic billing and regional policies.
- **Double wrapping**: bridges can obscure errors—log at the pipe level.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
