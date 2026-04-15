# Stack: In-chat PDF helpers

## Goal

Do **light PDF work inside chat** (view, basic edits in context) without leaving Open WebUI—pairs well with a broader [RAG workbench](rag-workbench.md) when documents are central.

## Components (community examples)

| Role | Item | Source |
|------|------|--------|
| Function | PDF Tools — rich UI for in-context basic editing | [openwebui.com](https://openwebui.com/f/jeffgranado/pdf_tools_rich_ui_for_in_context_basic_editing_2b4f9a26) |

## How it fits together

1. Install the PDF function and test on **non-sensitive** files first.
2. For large corpora or retrieval quality, add a **knowledge base** path per [rag-workbench.md](rag-workbench.md)—this stack is for interactive PDF UX, not full RAG.

## Trade-offs

- **Scope**: “basic editing” ≠ compliance-grade redaction—verify for your use case.
- **Size limits**: big PDFs can hit memory and latency limits.

## Status

Illustrative stack from a [community search sample](../docs/openwebui-import.md).
