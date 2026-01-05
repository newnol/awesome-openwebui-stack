# Chat Utilities

Các hàm để gọi chat completion trong Open WebUI.

## Import

```python
from open_webui.utils.chat import generate_chat_completion
```

## `generate_chat_completion()`

Hàm chính để gọi model completion. Tự động route đến đúng backend (OpenAI, Ollama, hoặc Pipe).

### Signature

```python
async def generate_chat_completion(
    request: Request,
    form_data: dict,
    user: Any,
    bypass_filter: bool = False,
) -> Union[dict, StreamingResponse]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `Request` | FastAPI Request object (lấy từ `__request__`) |
| `form_data` | `dict` | Request body với model, messages, stream, etc. |
| `user` | `UserModel` | User object |
| `bypass_filter` | `bool` | Bỏ qua access control filter |

### Request Body Format

```python
form_data = {
    "model": "gpt-4o",  # Open WebUI model ID
    "messages": [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello!"},
    ],
    "stream": True,  # or False
    "temperature": 0.7,
    "max_tokens": 4096,
}
```

### User Object

Cần tạo User object từ `__user__` dict:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    name: str
    role: str

# Trong pipe()
user_obj = User(
    id=__user__.get("id", ""),
    email=__user__.get("email", ""),
    name=__user__.get("name", ""),
    role=__user__.get("role", "user"),
)
```

### Return Value

**Non-streaming (`stream=False`):**
```python
{
    "id": "chatcmpl-xxx",
    "object": "chat.completion",
    "created": 1234567890,
    "model": "gpt-4o",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "Hello! How can I help?"
        },
        "finish_reason": "stop"
    }],
    "usage": {
        "prompt_tokens": 10,
        "completion_tokens": 20,
        "total_tokens": 30
    }
}
```

**Streaming (`stream=True`):**
Returns `StreamingResponse` with SSE format.

### Complete Example

```python
"""
title: Model Caller Example
"""

from pydantic import BaseModel, Field
from typing import Optional, Callable, Any, Awaitable

try:
    from open_webui.utils.chat import generate_chat_completion
    OPENWEBUI_AVAILABLE = True
except ImportError:
    OPENWEBUI_AVAILABLE = False


class Pipe:
    class Valves(BaseModel):
        TARGET_MODEL: str = Field(
            default="gpt-4o",
            description="Model to call"
        )
    
    def __init__(self):
        self.type = "pipe"
        self.id = "model_caller"
        self.name = "Model Caller"
        self.valves = self.Valves()
    
    def pipes(self):
        return [{"id": self.id, "name": self.name}]
    
    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[Any], Awaitable[None]] = None,
        __request__: Any = None,
        **kwargs
    ):
        if not OPENWEBUI_AVAILABLE:
            return "Error: Not running in Open WebUI"
        
        # Create User object
        class User(BaseModel):
            id: str
            email: str
            name: str
            role: str
        
        user_obj = User(
            id=__user__.get("id", "") if __user__ else "",
            email=__user__.get("email", "") if __user__ else "",
            name=__user__.get("name", "") if __user__ else "",
            role=__user__.get("role", "user") if __user__ else "user",
        )
        
        # Prepare request
        request_body = {
            "model": self.valves.TARGET_MODEL,
            "messages": body.get("messages", []),
            "stream": body.get("stream", False),
        }
        
        # Call model
        response = await generate_chat_completion(
            __request__,
            request_body,
            user_obj,
        )
        
        # Handle response
        if body.get("stream", False):
            # Return streaming generator
            async def stream():
                if hasattr(response, 'body_iterator'):
                    async for chunk in response.body_iterator:
                        yield chunk
            return stream()
        else:
            # Return content from dict response
            if isinstance(response, dict):
                return response.get("choices", [{}])[0].get("message", {}).get("content", "")
            return str(response)
```

## Routing Logic

`generate_chat_completion()` tự động route dựa trên model type:

1. **Pipe model** (`model.get("pipe")`) → `generate_function_chat_completion()`
2. **Ollama model** (`owned_by == "ollama"`) → `generate_ollama_chat_completion()`
3. **Arena model** (`owned_by == "arena"`) → Random chọn model rồi gọi lại
4. **OpenAI/Other** → `generate_openai_chat_completion()`

## Response Handling

### Non-streaming Response

```python
response = await generate_chat_completion(request, form_data, user)
content = response["choices"][0]["message"]["content"]
```

### Streaming Response (SSE)

```python
import json

response = await generate_chat_completion(request, form_data, user)

async def parse_stream():
    async for chunk in response.body_iterator:
        if isinstance(chunk, bytes):
            chunk = chunk.decode('utf-8')
        
        for line in chunk.split('\n'):
            line = line.strip()
            if line.startswith('data: '):
                data_str = line[6:]
                if data_str == '[DONE]':
                    break
                try:
                    data = json.loads(data_str)
                    content = data["choices"][0]["delta"].get("content", "")
                    if content:
                        yield content
                except json.JSONDecodeError:
                    pass
```

## Best Practices

1. **Always check if running in Open WebUI:**
   ```python
   try:
       from open_webui.utils.chat import generate_chat_completion
       OPENWEBUI_AVAILABLE = True
   except ImportError:
       OPENWEBUI_AVAILABLE = False
   ```

2. **Copy body parameters:**
   ```python
   request_body = {
       "model": target_model,
       "messages": body.get("messages", []),
       "stream": body.get("stream", False),
   }
   # Copy optional params
   for key in ["temperature", "max_tokens", "top_p"]:
       if body.get(key) is not None:
           request_body[key] = body.get(key)
   ```

3. **Handle both streaming and non-streaming:**
   ```python
   if body.get("stream", False):
       return stream_generator()
   else:
       return content_string
   ```
