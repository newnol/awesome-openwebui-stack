# Stack: Research agent

## Goal

Combine **retrieval**, **summarization**, and **clear sourcing** so answers can be checked—not a black box.

## Typical use cases

- Literature and web-assisted desk research
- Turning video content into quotable text (when licensing permits)

## Recommended components (pattern)

| Layer | Role |
|-------|------|
| Search | Provider-specific tool or API (add to [integrations](../catalog/integrations.md)) |
| Model | Strong reasoning + willingness to say “unknown” |
| Tools | Transcript/metadata tools when video is a source |
| Policies | Org rules on allowed domains and PII |

## In-repo examples

- [YouTube Transcript](../tools/youtube_transcript/youtube_transcript.py)
- [YouTube Info](../tools/youtube_info/youtube_info.py)

See [catalog/tools.md](../catalog/tools.md).

## Trade-offs

- **Automation vs. accuracy:** browsing tools need guardrails; rate limits apply.
- **Copyright and ToS:** remind users they are responsible for how they use third-party content.

## Where to find code or deploy guidance

- [categories/research.md](../categories/research.md)
- [catalog/learning-resources.md](../catalog/learning-resources.md)
