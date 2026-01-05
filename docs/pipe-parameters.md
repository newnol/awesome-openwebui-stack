# Pipe Parameters

Tài liệu về các tham số có sẵn trong hàm `pipe()` của Open WebUI.

## Signature đầy đủ

```python
async def pipe(
    self,
    body: dict,
    __user__: Optional[dict] = None,
    __event_emitter__: Callable[[Any], Awaitable[None]] = None,
    __event_call__: Callable[[Any], Awaitable[Any]] = None,
    __request__: Any = None,
    __model__: Optional[dict] = None,
    __chat_id__: Optional[str] = None,
    __session_id__: Optional[str] = None,
    __message_id__: Optional[str] = None,
    __task__: Optional[str] = None,
    __task_body__: Optional[dict] = None,
    __files__: Optional[list] = None,
    __metadata__: Optional[dict] = None,
    __tools__: Optional[dict] = None,
    __oauth_token__: Optional[dict] = None,
) -> Union[str, Generator, AsyncGenerator]:
```

## Chi tiết từng tham số

### `body: dict`
Request body chứa messages và các tham số.

```python
{
    "model": "model_id",
    "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
    ],
    "stream": True,  # or False
    "temperature": 0.7,
    "max_tokens": 4096,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}
```

### `__user__: dict`
Thông tin user hiện tại.

```python
{
    "id": "user-uuid-here",
    "email": "user@example.com",
    "name": "User Name",
    "role": "user",  # hoặc "admin"
    "valves": {...}  # UserValves nếu có
}
```

**Truy cập UserValves:**
```python
if __user__ and "valves" in __user__:
    user_valves = self.UserValves(**__user__["valves"])
```

### `__event_emitter__: Callable`
Hàm emit status updates lên UI.

```python
# Emit progress
await __event_emitter__({
    "type": "status",
    "data": {
        "status": "in_progress",  # "success", "error"
        "description": "Processing...",
        "done": False  # True khi hoàn thành
    }
})

# Emit message content
await __event_emitter__({
    "type": "message",
    "data": {
        "content": "Generated text..."
    }
})
```

### `__event_call__: Callable`
Gọi và chờ response từ WebSocket event.

```python
result = await __event_call__({
    "type": "request:chat:completion",
    "data": {...}
})
```

### `__request__: Request`
FastAPI Request object, chứa app state và metadata.

```python
# Access models
models = __request__.app.state.MODELS

# Access config
config = __request__.app.state.config
```

### `__model__: dict`
Thông tin model đang được gọi.

```python
{
    "id": "model_id",
    "name": "Model Name",
    "owned_by": "openai",  # hoặc "ollama", "arena"
    "pipe": {"type": "pipe"},  # nếu là pipe
    "info": {
        "meta": {
            "filterIds": [...],
            "model_ids": [...]
        }
    }
}
```

### `__chat_id__: str`
ID của cuộc chat hiện tại.

### `__session_id__: str`
Session ID của WebSocket connection.

### `__message_id__: str`
ID của message đang xử lý.

### `__task__: str`
Task type (nếu có), ví dụ: `"title_generation"`, `"tags_generation"`.

### `__task_body__: dict`
Task-specific data.

### `__files__: list`
Danh sách files đính kèm.

```python
[
    {
        "id": "file-uuid",
        "filename": "document.pdf",
        "data": {...},
        "meta": {...}
    }
]
```

### `__metadata__: dict`
Metadata từ request.

```python
{
    "chat_id": "...",
    "message_id": "...",
    "session_id": "...",
    "user_id": "...",
    "filter_ids": [...],
    "files": [...],
    "tool_ids": [...]
}
```

### `__tools__: dict`
Tools có sẵn cho function calling.

### `__oauth_token__: dict`
OAuth token nếu user login qua OAuth.

```python
{
    "access_token": "...",
    "refresh_token": "...",
    "expires_at": ...
}
```

## Return Types

### String Response
```python
return "This is the response"
```

### Streaming Response (Generator)
```python
def pipe(self, body, ...):
    def stream_generator():
        for chunk in ["Hello", " ", "World"]:
            yield chunk
    return stream_generator()
```

### Async Streaming Response
```python
async def pipe(self, body, ...):
    async def stream_generator():
        for chunk in ["Hello", " ", "World"]:
            yield chunk
    return stream_generator()
```

### Dict Response (OpenAI format)
```python
return {
    "choices": [{
        "message": {
            "role": "assistant",
            "content": "Response text"
        },
        "finish_reason": "stop"
    }]
}
```
