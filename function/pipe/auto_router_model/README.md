# Auto Router Model Pipe

🔀 **Automatically route requests to the best model based on keyword matching.**

This Open WebUI Pipe analyzes user prompts and dynamically selects the most appropriate model based on configurable keyword rules. Perfect for organizations that want to optimize costs by routing simple queries to cheaper models while complex tasks go to more capable ones.

## Features

- ✅ **Keyword-based routing** - Route requests based on keywords in user messages
- ✅ **Multi-provider support** - Works with Ollama, OpenAI, OpenRouter via LiteLLM
- ✅ **Streaming support** - Full streaming response support
- ✅ **User overrides** - Users can override routing with preferred models
- ✅ **Status updates** - Shows which model is being used in the UI
- ✅ **Vietnamese support** - Works with Unicode/Vietnamese keywords

## Installation

### 1. Install LiteLLM

In your Open WebUI Docker container:

```bash
pip install litellm
```

Or add to your `requirements.txt`.

### 2. Add the Pipe

1. Go to **Admin Panel** → **Functions** → **Pipes**
2. Click **Create new pipe**
3. Copy the content of `auto_router_model.py`
4. Save and enable the pipe

## Configuration

### Valves (Admin Settings)

| Field | Default | Description |
|-------|---------|-------------|
| `OPENAI_API_BASE` | `http://host.docker.internal:11434/v1` | API endpoint URL |
| `OPENAI_API_KEY` | `ollama` | API key for the endpoint |
| `ROUTER_CONFIG` | See below | JSON routing configuration |
| `FALLBACK_MODEL_ID` | `llama3.2:latest` | Default model when no keywords match |
| `DEBUG` | `false` | Enable debug logs in console |
| `status` | `true` | Show routing status in UI |

### ROUTER_CONFIG Format

```json
[
    {
        "model_id": "codellama:latest",
        "keywords": ["code", "python", "javascript", "debug", "programming"],
        "description": "Coding tasks"
    },
    {
        "model_id": "gpt-4o",
        "keywords": ["analyze", "complex", "reasoning", "explain"],
        "description": "Complex reasoning"
    },
    {
        "model_id": "claude-3-5-sonnet",
        "keywords": ["write", "creative", "story", "essay"],
        "description": "Creative writing"
    },
    {
        "model_id": "llama3.2:latest",
        "keywords": ["math", "calculate", "số", "tính"],
        "description": "Math tasks"
    }
]
```

### UserValves (Per-User Settings)

Users can override the routing behavior:

| Field | Default | Description |
|-------|---------|-------------|
| `preferred_model` | `""` | Always use this model (bypasses routing) |
| `disable_routing` | `false` | Disable routing, always use fallback |

## How It Works

```
┌──────────────────┐
│   User Message   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Analyze Message │
│  for Keywords    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌─────────────────┐
│  Match Found?    │─No─▶│  Use Fallback   │
└────────┬─────────┘     │     Model       │
         │Yes            └─────────────────┘
         ▼
┌──────────────────┐
│  Select Model    │
│  with Most       │
│  Keyword Matches │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Route to        │
│  Selected Model  │
│  via LiteLLM     │
└──────────────────┘
```

## API Base URLs

| Provider | API Base URL |
|----------|--------------|
| **Ollama (Docker)** | `http://host.docker.internal:11434/v1` |
| **Ollama (Linux)** | `http://172.17.0.1:11434/v1` |
| **Ollama (same host)** | `http://localhost:11434/v1` |
| **OpenAI** | `https://api.openai.com/v1` |
| **OpenRouter** | `https://openrouter.ai/api/v1` |

## Examples

### Example 1: Route coding questions to CodeLlama

**Config:**
```json
[{"model_id": "codellama:latest", "keywords": ["code", "python", "function"], "description": "Code"}]
```

**User:** "Help me write a python function to sort a list"  
**Result:** Routes to `codellama:latest` (matches: python, function, code)

### Example 2: Multi-language support

**Config:**
```json
[{"model_id": "math-model", "keywords": ["tính", "số", "phép tính", "math"], "description": "Math"}]
```

**User:** "Tính tổng các số từ 1 đến 100"  
**Result:** Routes to `math-model` (matches: tính, số)

## Troubleshooting

### "LiteLLM is not installed"

Run inside the Open WebUI container:
```bash
docker exec -it open-webui pip install litellm
```

### "Configuration Error: Invalid JSON"

Check your `ROUTER_CONFIG` JSON syntax. Common issues:
- Missing commas between array items
- Using single quotes instead of double quotes
- Trailing commas

### Model not found

Ensure the `model_id` matches exactly what's available in your provider:
- For Ollama: Use `ollama list` to see available models
- For OpenAI: Use standard model names like `gpt-4o`, `gpt-3.5-turbo`

## Running Tests

```bash
cd function/pipe/auto_router_model
python test_auto_router.py
```

Expected output:
```
Ran 26 tests in 0.002s
OK
✅ All tests passed!
```

## License

MIT License - Feel free to use and modify!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request
