# Tools

Python tools you can register in Open WebUI (see [official tools docs](https://docs.openwebui.com/features/plugin/tools/)).

## In this repository (reference samples)

### [YouTube Transcript](../tools/youtube_transcript/youtube_transcript.py)
- **Purpose:** Fetch transcripts from YouTube by URL or video ID.
- **Best for:** Research, note-taking, quoted evidence from video content.
- **Category:** Research, Productivity
- **Stack fit:** [Research agent](../stacks/research-agent.md)
- **Status:** Sample — verify before production use
- **Notes:** Requires `youtube-transcript-api`. See [tools/README.md](../tools/README.md).

### [YouTube Info](../tools/youtube_info/youtube_info.py)
- **Purpose:** Extract title and description from YouTube pages (Selenium-based).
- **Best for:** Metadata for research workflows.
- **Category:** Research
- **Stack fit:** [Research agent](../stacks/research-agent.md)
- **Status:** Sample — headless browser dependency
- **Notes:** Requires `selenium` and a suitable browser/driver setup.

### [Diagram Generator](../tools/diagram_generator/diagram_generator.py)
- **Purpose:** Generate architecture diagrams from Python using the `diagrams` library.
- **Best for:** Visualizing systems, cloud diagrams from code.
- **Category:** Coding, Productivity
- **Stack fit:** [Coding assistant](../stacks/coding-assistant.md)
- **Status:** Sample
- **Notes:** Requires Graphviz system packages. See [DIAGRAM_GENERATOR_README.md](../tools/diagram_generator/DIAGRAM_GENERATOR_README.md).

### [Auto Tool Filter](../tools/auto_tool_filter/auto_tool_filter.py)
- **Purpose:** Use an LLM to pick relevant tools from a larger toolset for a query.
- **Best for:** Reducing noise when many tools are enabled.
- **Category:** Multi-agent, Automation
- **Stack fit:** [Coding assistant](../stacks/coding-assistant.md) when many tools are enabled
- **Status:** Sample

---

## Community and upstream (additions welcome)

Submit entries via [CONTRIBUTING.md](../CONTRIBUTING.md). Prefer links to maintained repositories with clear licenses.

| Name | Purpose | Best for | Source |
|------|---------|----------|--------|
| *Your tool* | *One line* | *Use cases* | *Link* |
