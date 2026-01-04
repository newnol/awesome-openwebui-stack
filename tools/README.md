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

---

### Tool: `openwebui_download_boost.py`

**Purpose**  
Sends POST requests to OpenWebUI API to boost the download count for posts/applications. This tool simulates download actions by calling the OpenWebUI download endpoint.

**Main components**

- `Tools` class with:
  - `Valves` / `UserValves` (Pydantic models) for configuration.
  - `boost_download_count(...)` async method, which is the entrypoint for Open WebUI.
- `EventEmitter` helper to stream status updates (`in_progress`, `success`, `error`) back to the Open WebUI UI.
- Internal helper `_send_download_request_sync(...)` which sends HTTP POST requests using `requests` library.

---

### Dependencies

Install the required Python package:

```bash
pip install requests
```

The file uses:

- `requests` – to send HTTP POST requests to the OpenWebUI API endpoint.

---

### How it works

1. **Input**: A post/application ID (UUID format) and optional count parameter.
2. The tool:
   - Validates the post ID and authorization token.
   - Constructs the API URL: `https://api.openwebui.com/api/v1/posts/{post_id}/download`
   - Sends one or multiple POST requests with all required headers (including Bearer token authentication).
   - Adds configurable delay between requests to avoid rate limiting.
   - Returns aggregated results including success/failure counts and status code distribution.
3. **Output** (to Open WebUI): a **string** containing the request results, including:
   - Total success/failure counts
   - Success rate percentage
   - Status code distribution (for multiple requests)
   - Details of the first/last request

---

### Configuration

Before using this tool, you need to configure the authorization token:

1. **Get your Bearer token**:
   - Log in to OpenWebUI (https://openwebui.com)
   - Open browser Developer Tools (F12)
   - Go to Network tab
   - Make a request to the API (or check an existing request)
   - Find the `authorization` header in the request headers
   - Copy the token value (the part after "Bearer ")

2. **Set the token in UserValves**:
   - In Open WebUI, go to tool settings
   - Set `AUTHORIZATION_TOKEN` in UserValves to your Bearer token
   - Optionally set `CUSTOM_USER_AGENT` if you want to use a different user agent
   - Optionally set `DELAY_BETWEEN_REQUESTS` (default: 0.1 seconds) to control delay between multiple requests. Set to 0 for maximum speed.
   - Optionally set `CONCURRENT_REQUESTS` (default: 10, max: 50) to control how many requests run simultaneously. Higher = faster but may hit rate limits.

---

### Open WebUI integration

The file is designed to be used as a Python tool in Open WebUI with the following characteristics:

- **Metadata** (in the top-of-file docstring):
  - `title`: `OpenWebUI Download Boost`
  - `author`: `newnol`
  - `requirements`: `requests`
- **Entrypoint**: `Tools().boost_download_count`

Example behavior in chat:

- User:  
  "Boost download count for post 1f0be869-4e6b-49c5-b4e7-98012ab53711"
- The model:
  - Calls the tool `boost_download_count` with the post ID (count defaults to 1).
  - Sends POST request(s) to OpenWebUI API.
  - Returns the result showing success or failure.

- User:  
  "Boost download count 100 times for post 1f0be869-4e6b-49c5-b4e7-98012ab53711"
- The model:
  - Calls the tool `boost_download_count` with post_id and count=100.
  - Sends 100 POST requests with delay between each request.
  - Returns aggregated results with success/failure statistics.

---

### Local CLI testing

You can test the tool from the command line:

```bash
python tools/openwebui_download_boost.py <post_id> <authorization_token> [count] [custom_user_agent] [delay]
```

Examples:

**Single request:**
```bash
python tools/openwebui_download_boost.py "1f0be869-4e6b-49c5-b4e7-98012ab53711" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**100 requests (fast mode, 10 concurrent, 0.1s delay):**
```bash
python tools/openwebui_download_boost.py "1f0be869-4e6b-49c5-b4e7-98012ab53711" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." 100
```

**100 requests (maximum speed, 20 concurrent, no delay):**
```bash
python tools/openwebui_download_boost.py "1f0be869-4e6b-49c5-b4e7-98012ab53711" "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." 100 0 20
```

This prints the result of the request(s) including status code, success/failure counts, and response data.

**Note**: Make sure you have the `requests` package installed before running:
```bash
pip install requests
```


