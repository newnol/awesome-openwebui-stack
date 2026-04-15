# Stack: Coding sandbox + tool debugging

## Goal

**Run code in chat**, **inspect what tools see** in context, and optionally **parallelize** tool use—good for builders and admins tuning toolsets.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Tool | Open WebUI Code Execution Tools | [openwebui.com](https://openwebui.com/posts/618a6082-f1be-49c6-aa66-f3554beb5330) |
| Tool | Tools Context Inspector | [openwebui.com](https://openwebui.com/posts/519c365f-dadd-4ca9-a2ce-7a5a582b7194) |
| Tool | Parallel Tools | [openwebui.com](https://openwebui.com/posts/1d44cfce-d810-49b1-bbcb-52cea19c2dcf) |

## How it fits together

1. Enable **Code Execution Tools** for snippets/scripts the model can run (per your security policy).
2. Use **Tools Context Inspector** when something “mysterious” happens with tool I/O.
3. Add **Parallel Tools** if latency from sequential tools is painful.

## Trade-offs

- **Security**: code execution is high risk—sandbox, network policy, and allowlists matter.
- **Noise**: inspectors add tokens; use when debugging, not every session.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
