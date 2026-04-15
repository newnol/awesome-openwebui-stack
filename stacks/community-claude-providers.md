# Stack: Claude-focused providers + bridges

## Goal

Standardize on **Anthropic** models inside Open WebUI while optionally **bridging** tool formats or mixing provider APIs—useful when your org standardizes on Claude but still uses OpenAI-compatible stacks elsewhere.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Function | Anthropic API Integration (Claude 4 / 4.5 / Opus + tools) | [openwebui.com](https://openwebui.com/f/bermont/anthropic_api_integration_claude_4_45_opus_45_exte_1a167991) |
| Pipe / function | Claude OpenAI Tools Bridge Pipe | [openwebui.com](https://openwebui.com/f/jiangnangenius/anthropic_7e79c01f) |

## How it fits together

1. Configure **Anthropic API Integration** with org keys and model allowlist.
2. Add the **bridge** only if you need OpenAI-style tool calling interop—otherwise keep one path to reduce bugs.

## Trade-offs

- **Vendor lock-in**: Claude + Anthropic billing and regional policies.
- **Double wrapping**: bridges can obscure errors—log at the pipe level.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
