# Filter Functions

Hướng dẫn viết Filter (inlet/outlet) trong Open WebUI.

## Filter là gì?

Filter là function xử lý request/response:
- **Inlet**: Xử lý request TRƯỚC khi gửi đến model
- **Outlet**: Xử lý response SAU khi nhận từ model

## Cấu trúc cơ bản

```python
"""
title: My Filter
author: your_name
version: 0.1.0
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        """System configuration"""
        priority: int = Field(
            default=0,
            description="Filter priority (higher = runs first)"
        )
        enabled: bool = Field(
            default=True,
            description="Enable this filter"
        )
    
    class UserValves(BaseModel):
        """User configuration"""
        custom_setting: str = Field(
            default="",
            description="User-specific setting"
        )
    
    def __init__(self):
        self.valves = self.Valves()
        # Optional: Set toggle=True to make filter toggleable per-chat
        # self.toggle = True
    
    async def inlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __request__: Optional[Any] = None,
        __model__: Optional[dict] = None,
        __event_emitter__: Optional[Callable] = None,
    ) -> dict:
        """
        Process request before sending to model.
        MUST return modified body dict.
        """
        # Your processing logic
        return body
    
    async def outlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __request__: Optional[Any] = None,
        __model__: Optional[dict] = None,
        __event_emitter__: Optional[Callable] = None,
    ) -> dict:
        """
        Process response before sending to user.
        MUST return modified body dict.
        """
        # Your processing logic
        return body
```

## Inlet Function

### Parameters

```python
async def inlet(
    self,
    body: dict,                      # Request body
    __user__: dict = None,           # User info
    __request__: Request = None,     # FastAPI Request
    __model__: dict = None,          # Model info
    __event_emitter__: Callable = None,  # Status emitter
    __id__: str = None,              # Filter ID
    __metadata__: dict = None,       # Request metadata
) -> dict:
```

### Body Structure (Input)

```python
{
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
    ],
    "stream": True,
    "temperature": 0.7,
    # ... other params
}
```

### Common Use Cases

#### 1. Modify System Prompt

```python
async def inlet(self, body: dict, **kwargs) -> dict:
    messages = body.get("messages", [])
    
    # Add system prompt if not exists
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant."
        })
    else:
        # Append to existing
        messages[0]["content"] += "\n\nBe concise in your responses."
    
    body["messages"] = messages
    return body
```

#### 2. Add Context to User Message

```python
async def inlet(self, body: dict, **kwargs) -> dict:
    messages = body.get("messages", [])
    
    if messages:
        last_msg = messages[-1]
        if last_msg.get("role") == "user":
            context = f"[Time: {datetime.now()}]\n"
            last_msg["content"] = context + last_msg["content"]
    
    return body
```

#### 3. Filter/Validate Input

```python
async def inlet(self, body: dict, __event_emitter__=None, **kwargs) -> dict:
    messages = body.get("messages", [])
    
    # Check for blocked words
    blocked_words = ["spam", "hack"]
    user_content = messages[-1].get("content", "").lower() if messages else ""
    
    for word in blocked_words:
        if word in user_content:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {
                        "status": "error",
                        "description": f"Blocked word detected: {word}",
                        "done": True
                    }
                })
            raise Exception(f"Input contains blocked word: {word}")
    
    return body
```

#### 4. Modify Model Parameters

```python
async def inlet(self, body: dict, **kwargs) -> dict:
    # Force certain parameters
    body["temperature"] = 0.7
    body["max_tokens"] = 2000
    
    # Remove certain parameters
    body.pop("frequency_penalty", None)
    
    return body
```

## Outlet Function

### Body Structure (Output)

```python
{
    "model": "gpt-4o",
    "messages": [
        # Original messages + assistant response
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "Response from model"},
    ],
    "chat_id": "...",
    "id": "...",  # Message ID
    "session_id": "...",
}
```

### Common Use Cases

#### 1. Log Responses

```python
async def outlet(self, body: dict, __user__=None, **kwargs) -> dict:
    messages = body.get("messages", [])
    
    if messages:
        last_msg = messages[-1]
        if last_msg.get("role") == "assistant":
            user_id = __user__.get("id") if __user__ else "unknown"
            print(f"[{user_id}] Response: {last_msg['content'][:100]}...")
    
    return body
```

#### 2. Post-process Response

```python
async def outlet(self, body: dict, **kwargs) -> dict:
    messages = body.get("messages", [])
    
    if messages:
        last_msg = messages[-1]
        if last_msg.get("role") == "assistant":
            # Add disclaimer
            last_msg["content"] += "\n\n---\n*This is AI-generated content.*"
    
    return body
```

#### 3. Analytics/Metrics

```python
async def outlet(self, body: dict, __user__=None, **kwargs) -> dict:
    # Count tokens, track usage, etc.
    messages = body.get("messages", [])
    
    total_chars = sum(len(m.get("content", "")) for m in messages)
    
    # Log or send to analytics service
    print(f"Total characters: {total_chars}")
    
    return body
```

## File Handler

Để skip file processing trong inlet:

```python
class Filter:
    def __init__(self):
        self.valves = self.Valves()
        self.file_handler = True  # Skip automatic file handling
    
    async def inlet(self, body: dict, **kwargs) -> dict:
        # Handle files manually
        metadata = body.get("metadata", {})
        files = metadata.get("files", [])
        
        for file in files:
            # Process file
            pass
        
        return body
```

## Toggle Filter

Cho phép user bật/tắt filter per-chat:

```python
class Filter:
    def __init__(self):
        self.valves = self.Valves()
        self.toggle = True  # Enable toggle in UI
    
    async def inlet(self, body: dict, **kwargs) -> dict:
        # This filter can be toggled on/off by user
        return body
```

## Priority

Filter với priority cao hơn chạy trước:

```python
class Valves(BaseModel):
    priority: int = Field(
        default=10,  # Higher = runs first
        description="Filter priority"
    )
```

## Complete Example: Content Moderation Filter

```python
"""
title: Content Moderation Filter
author: example
version: 0.1.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Callable, Any
import re


class Filter:
    class Valves(BaseModel):
        priority: int = Field(default=100, description="High priority")
        blocked_patterns: str = Field(
            default="spam|hack|exploit",
            description="Regex patterns to block (pipe-separated)"
        )
        max_message_length: int = Field(
            default=10000,
            description="Maximum message length"
        )
    
    def __init__(self):
        self.valves = self.Valves()
    
    async def inlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable] = None,
        **kwargs
    ) -> dict:
        messages = body.get("messages", [])
        
        if not messages:
            return body
        
        last_msg = messages[-1]
        content = last_msg.get("content", "")
        
        # Check length
        if len(content) > self.valves.max_message_length:
            raise Exception(
                f"Message too long ({len(content)} chars). "
                f"Max: {self.valves.max_message_length}"
            )
        
        # Check blocked patterns
        if self.valves.blocked_patterns:
            pattern = re.compile(
                self.valves.blocked_patterns,
                re.IGNORECASE
            )
            if pattern.search(content):
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {
                            "status": "error",
                            "description": "Message contains blocked content",
                            "done": True
                        }
                    })
                raise Exception("Message contains blocked content")
        
        return body
    
    async def outlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        **kwargs
    ) -> dict:
        # Log for audit
        messages = body.get("messages", [])
        if messages and messages[-1].get("role") == "assistant":
            print(f"[Audit] Response generated for user: {__user__.get('id')}")
        
        return body
```
