# Event Emitter

Gửi status updates và messages đến UI từ Pipe/Filter.

## Import

Event emitter được pass vào function qua parameter `__event_emitter__`.

## Basic Usage

```python
async def pipe(
    self,
    body: dict,
    __event_emitter__: Callable[[Any], Awaitable[None]] = None,
    **kwargs
):
    if __event_emitter__:
        await __event_emitter__({
            "type": "status",
            "data": {
                "status": "in_progress",
                "description": "Processing...",
                "done": False
            }
        })
```

## Event Types

### Status Event

Hiển thị status message trong UI.

```python
await __event_emitter__({
    "type": "status",
    "data": {
        "status": "in_progress",  # "success", "error"
        "description": "Processing your request...",
        "done": False  # True khi hoàn thành
    }
})
```

**Status values:**
- `"in_progress"` - Đang xử lý (spinner)
- `"success"` - Hoàn thành (checkmark)
- `"error"` - Lỗi (X icon)

### Message Event

Gửi content trực tiếp đến chat.

```python
await __event_emitter__({
    "type": "message",
    "data": {
        "content": "Here is some generated text..."
    }
})
```

### Citation Event

Thêm citation/source vào response.

```python
await __event_emitter__({
    "type": "citation",
    "data": {
        "document": ["Source document content..."],
        "metadata": [{"source": "document.pdf"}],
        "source": {"name": "document.pdf"}
    }
})
```

## Helper Class

Tạo class helper để dễ sử dụng:

```python
from typing import Callable, Any, Awaitable


class EventEmitter:
    """Helper class for emitting events to Open WebUI."""
    
    def __init__(self, event_emitter: Callable[[dict], Awaitable[None]] = None):
        self.event_emitter = event_emitter
    
    async def emit(
        self,
        description: str = "",
        status: str = "in_progress",
        done: bool = False
    ) -> None:
        """Emit a status event."""
        if self.event_emitter:
            await self.event_emitter({
                "type": "status",
                "data": {
                    "status": status,
                    "description": description,
                    "done": done
                }
            })
    
    async def progress(self, description: str) -> None:
        """Emit progress status."""
        await self.emit(description, "in_progress", False)
    
    async def success(self, description: str) -> None:
        """Emit success status."""
        await self.emit(description, "success", True)
    
    async def error(self, description: str) -> None:
        """Emit error status."""
        await self.emit(description, "error", True)
    
    async def message(self, content: str) -> None:
        """Emit message content."""
        if self.event_emitter:
            await self.event_emitter({
                "type": "message",
                "data": {"content": content}
            })
    
    async def citation(
        self,
        document: list,
        metadata: list,
        source_name: str
    ) -> None:
        """Emit citation."""
        if self.event_emitter:
            await self.event_emitter({
                "type": "citation",
                "data": {
                    "document": document,
                    "metadata": metadata,
                    "source": {"name": source_name}
                }
            })
```

## Usage in Pipe

```python
class Pipe:
    async def pipe(
        self,
        body: dict,
        __event_emitter__: Callable = None,
        **kwargs
    ):
        emitter = EventEmitter(__event_emitter__)
        
        # Show progress
        await emitter.progress("🔍 Analyzing your request...")
        
        try:
            # Do something
            result = await self.process(body)
            
            # Show success
            await emitter.success("✅ Processing complete!")
            
            return result
            
        except Exception as e:
            # Show error
            await emitter.error(f"❌ Error: {str(e)}")
            return f"Error: {str(e)}"
```

## Usage in Filter

```python
class Filter:
    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable = None,
        **kwargs
    ) -> dict:
        emitter = EventEmitter(__event_emitter__)
        
        await emitter.progress("🔒 Validating input...")
        
        # Validate
        if not self.validate(body):
            await emitter.error("❌ Validation failed")
            raise Exception("Validation failed")
        
        await emitter.success("✅ Input validated")
        return body
```

## Progress Steps

Hiển thị tiến trình multi-step:

```python
async def pipe(self, body: dict, __event_emitter__=None, **kwargs):
    emitter = EventEmitter(__event_emitter__)
    
    steps = [
        ("🔍 Analyzing...", self.analyze),
        ("🧠 Processing...", self.process),
        ("📝 Generating...", self.generate),
    ]
    
    for i, (description, func) in enumerate(steps):
        await emitter.progress(f"[{i+1}/{len(steps)}] {description}")
        result = await func(body)
    
    await emitter.success("✅ Complete!")
    return result
```

## Streaming with Status

Kết hợp streaming và status updates:

```python
async def pipe(self, body: dict, __event_emitter__=None, **kwargs):
    emitter = EventEmitter(__event_emitter__)
    
    await emitter.progress("🚀 Starting generation...")
    
    async def stream_with_status():
        try:
            for chunk in generate_chunks():
                yield chunk
            
            await emitter.success("✅ Generation complete!")
        except Exception as e:
            await emitter.error(f"❌ Error: {e}")
            yield f"\n\nError: {e}"
    
    return stream_with_status()
```

## Event Call

`__event_call__` cho phép gọi và chờ response:

```python
async def pipe(
    self,
    body: dict,
    __event_call__: Callable = None,
    **kwargs
):
    if __event_call__:
        # Call and wait for response
        result = await __event_call__({
            "type": "request:chat:completion",
            "data": {
                "form_data": body,
                "model": model_info,
                "channel": channel_id,
            }
        })
        return result
```

## Complete Example

```python
"""
title: Status Demo Pipe
"""

from pydantic import BaseModel
from typing import Optional, Callable, Any, Awaitable
import asyncio


class EventEmitter:
    def __init__(self, emitter: Callable = None):
        self.emitter = emitter
    
    async def emit(self, desc: str, status: str = "in_progress", done: bool = False):
        if self.emitter:
            await self.emitter({
                "type": "status",
                "data": {"status": status, "description": desc, "done": done}
            })
    
    async def progress(self, desc: str):
        await self.emit(desc, "in_progress", False)
    
    async def success(self, desc: str):
        await self.emit(desc, "success", True)
    
    async def error(self, desc: str):
        await self.emit(desc, "error", True)


class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "status_demo"
        self.name = "Status Demo"
    
    def pipes(self):
        return [{"id": self.id, "name": self.name}]
    
    async def pipe(
        self,
        body: dict,
        __event_emitter__: Callable = None,
        **kwargs
    ):
        emitter = EventEmitter(__event_emitter__)
        
        # Step 1
        await emitter.progress("🔍 Step 1: Analyzing...")
        await asyncio.sleep(1)
        
        # Step 2
        await emitter.progress("🧠 Step 2: Processing...")
        await asyncio.sleep(1)
        
        # Step 3
        await emitter.progress("📝 Step 3: Generating...")
        await asyncio.sleep(1)
        
        # Done
        await emitter.success("✅ All steps complete!")
        
        return "Hello! This is a demo response."
```
