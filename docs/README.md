# Open WebUI Internal API Documentation

Tài liệu này tổng hợp các hàm và utilities có sẵn trong Open WebUI để sử dụng khi viết Functions (Pipes, Filters, Tools).

## Mục lục

1. [Pipe Parameters](./pipe-parameters.md) - Các tham số có sẵn trong hàm `pipe()`
2. [Chat Utilities](./chat-utilities.md) - Hàm gọi chat completion
3. [Message Utilities](./message-utilities.md) - Xử lý messages
4. [Embedding Utilities](./embedding-utilities.md) - Tạo embeddings
5. [Filter Functions](./filter-functions.md) - Viết filter inlet/outlet
6. [Event Emitter](./event-emitter.md) - Gửi status updates
7. [Examples](./examples/) - Ví dụ thực tế

## Quick Start

### Cấu trúc cơ bản của một Pipe

```python
"""
title: My Pipe
author: your_name
version: 0.1.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Callable, Any, Awaitable

class Pipe:
    class Valves(BaseModel):
        """System-level config"""
        MY_CONFIG: str = Field(default="value", description="...")
    
    class UserValves(BaseModel):
        """User-level config"""
        user_setting: str = Field(default="", description="...")
    
    def __init__(self):
        self.type = "pipe"
        self.id = "my_pipe"
        self.name = "My Pipe"
        self.valves = self.Valves()
    
    def pipes(self):
        """Return list of available pipes (manifold)"""
        return [{"id": self.id, "name": self.name}]
    
    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Callable[[Any], Awaitable[None]] = None,
        __request__: Any = None,
        __model__: Optional[dict] = None,
    ) -> str:
        # Your logic here
        return "Response"
```

### Import từ Open WebUI

```python
# Chat completion
from open_webui.utils.chat import generate_chat_completion

# Message utilities  
from open_webui.utils.misc import (
    get_last_user_message,
    get_last_assistant_message,
    add_or_update_system_message,
)

# Embeddings
from open_webui.utils.embeddings import generate_embeddings

# Models
from open_webui.models.functions import Functions
from open_webui.models.models import Models
```
