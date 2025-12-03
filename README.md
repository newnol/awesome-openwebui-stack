## Open WebUI Tools

Custom tools for Open WebUI.

---

## Tools

### YouTube Transcript (`youtube_transcript.py`)

Tool to fetch transcripts from YouTube videos.

**Features:**
- Fetch full transcript from YouTube video by URL or video ID
- Prefer Vietnamese language, fallback to English if not available
- Returns transcript as segments and full text

**Dependencies:**
```bash
pip install youtube-transcript-api
```

**File:** `tools/youtube_transcript.py`

---

### YouTube Info (`youtube_info.py`)

Tool to extract detailed information from YouTube videos (title, description).

**Features:**
- Extract full title and description from YouTube video
- Uses Selenium to access `ytInitialPlayerResponse` JavaScript variable
- Supports headless mode

**Dependencies:**
```bash
pip install selenium
```

**File:** `tools/youtube_info.py`

---

### Diagram Generator (`diagram_generator.py`)

Tool to generate cloud system architecture diagrams using the `diagrams` library.

**Features:**
- Generate cloud system architecture diagrams (AWS, GCP, Azure, Kubernetes, etc.)
- Accepts Python code to create diagrams
- Renders diagrams as image files (PNG, JPG, PDF, SVG)

**Dependencies:**
```bash
pip install diagrams
```

**System Requirements:**
- Graphviz (requires separate installation):
  - macOS: `brew install graphviz`
  - Ubuntu/Debian: `sudo apt-get install graphviz`
  - Windows: Download from https://graphviz.org/download/

**File:** `tools/diagram_generator.py`

**See also:** `tools/DIAGRAM_GENERATOR_README.md` for detailed usage and examples.

---

### Auto Tool Filter (`auto_tool_filter.py`)

Tool to automatically filter and select appropriate tools based on user query.

**Features:**
- Automatically analyze query and select appropriate tools
- Uses LLM to evaluate and filter tools
- Supports multi-tool selection when needed

**File:** `tools/auto_tool_filter.py`

---

## License

MIT
