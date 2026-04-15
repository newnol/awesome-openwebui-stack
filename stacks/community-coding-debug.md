# Stack: Coding sandbox + tool debugging

## Goal

**Run code in chat**, **inspect what tools see** in context, and optionally **parallelize** tool use—good for builders and admins tuning toolsets.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Tool | Open WebUI Code Execution Tools | [openwebui.com](https://openwebui.com/t/colton/open_webui_code_execution_tools_2o2_618a6082) |
| Tool | Tools Context Inspector | [openwebui.com](https://openwebui.com/t/jeffreysmith115076ab75/tools_context_inspector_519c365f) |
| Tool | Parallel Tools | [openwebui.com](https://openwebui.com/t/skyzi000/parallel_tools_1d44cfce) |

## How it fits together

1. Enable **Code Execution Tools** for snippets/scripts the model can run (per your security policy).
2. Use **Tools Context Inspector** when something “mysterious” happens with tool I/O.
3. Add **Parallel Tools** if latency from sequential tools is painful.

## Trade-offs

- **Security**: code execution is high risk—sandbox, network policy, and allowlists matter.
- **Noise**: inspectors add tokens; use when debugging, not every session.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
