## YouTube Transcript Tool

This folder contains custom tools used with Open WebUI.  
The first tool is a YouTube transcript provider implemented with `youtube-transcript-api`.

---

### Tool: `youtube_transcript.py`

**Purpose**  
Fetch the full transcript of a YouTube video (by URL or video ID) and return it as plain text, suitable for feeding into LLM prompts in Open WebUI.

**Main components**

- `Tools` class with:
  - `Valves` / `UserValves` (Pydantic models) for configuration.
  - `get_youtube_transcript(...)` async method, which is the entrypoint for Open WebUI.
- `EventEmitter` helper to stream status updates (`in_progress`, `success`, `error`) back to the Open WebUI UI.
- Internal helper `_fetch_youtube_transcript_structured(...)` which talks to `youtube-transcript-api`.

---

### Dependencies

Install the required Python package:

```bash
pip install youtube-transcript-api
```

The file uses:

- `youtube-transcript-api` – to fetch transcripts from YouTube without needing an official API key.  
  API style is based on the official docs:  
  `yt_api = YouTubeTranscriptApi(); yt_api.fetch(video_id, languages=[...])`

---

### How it works

1. **Input**: A YouTube URL or bare video ID.
2. The tool:
   - Extracts the video ID.
   - Chooses preferred languages from `UserValves.TRANSCRIPT_LANGUAGE` (default: `"vi,en"`).
   - Calls `YouTubeTranscriptApi().fetch(...)` with those languages.
   - Normalizes the response into:
     - `segments`: list of `{start, duration, text}`.
     - `full_text`: concatenation of all `text` lines.
3. **Output** (to Open WebUI): a **string** containing the full transcript text, ready for summarization or further processing by the model.

The low-level structured dict is used internally; the Open WebUI tool entrypoint returns only the transcript text for simplicity.

---

### Open WebUI integration

The file is designed to be used as a Python tool in Open WebUI with the following characteristics:

- **Metadata** (in the top-of-file docstring):
  - `title`: `Youtube Transcript Provider (youtube-transcript-api)`
  - `author`: `newnol`
  - `requirements`: `youtube-transcript-api`
- **Entrypoint**: `Tools().get_youtube_transcript`

Example behavior in chat:

- User:  
  “Get the YouTube transcript for this video and summarize it: https://www.youtube.com/watch?v=...”
- The model:
  - Calls the tool `get_youtube_transcript` with the URL.
  - Receives the full transcript text.
  - Uses that text to generate a summary / analysis.

---

### Local CLI testing

Although the main target is Open WebUI, you can also run the structured helper from the command line for quick checks:

```bash
python tools/youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" --language vi
```

This prints a JSON object with:

- `video_id`
- `language`
- `segments`
- `full_text`

This is useful for debugging and verifying that transcripts can be fetched correctly before wiring the tool into Open WebUI.


