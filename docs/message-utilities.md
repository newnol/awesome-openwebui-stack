# Message Utilities

Các hàm tiện ích để xử lý messages trong Open WebUI.

## Import

```python
from open_webui.utils.misc import (
    get_last_user_message,
    get_last_user_message_item,
    get_last_assistant_message,
    get_last_assistant_message_item,
    get_content_from_message,
    get_messages_content,
    get_system_message,
    remove_system_message,
    pop_system_message,
    add_or_update_system_message,
    add_or_update_user_message,
    prepend_to_first_user_message_content,
    append_or_update_assistant_message,
    update_message_content,
    replace_system_message_content,
)
```

## Lấy Messages

### `get_last_user_message(messages)`

Lấy nội dung text của message user cuối cùng.

```python
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "How are you?"},
]

last_msg = get_last_user_message(messages)
# Returns: "How are you?"
```

### `get_last_user_message_item(messages)`

Lấy message dict user cuối cùng.

```python
item = get_last_user_message_item(messages)
# Returns: {"role": "user", "content": "How are you?"}
```

### `get_last_assistant_message(messages)`

Lấy nội dung text của message assistant cuối cùng.

```python
last_assistant = get_last_assistant_message(messages)
# Returns: "Hi!"
```

### `get_last_assistant_message_item(messages)`

Lấy message dict assistant cuối cùng.

```python
item = get_last_assistant_message_item(messages)
# Returns: {"role": "assistant", "content": "Hi!"}
```

### `get_content_from_message(message)`

Trích xuất text content từ message (hỗ trợ cả text và multimodal).

```python
# Text message
msg = {"role": "user", "content": "Hello"}
content = get_content_from_message(msg)
# Returns: "Hello"

# Multimodal message
msg = {
    "role": "user", 
    "content": [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "..."}}
    ]
}
content = get_content_from_message(msg)
# Returns: "What's in this image?"
```

### `get_messages_content(messages)`

Nối tất cả messages thành một string.

```python
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
]
content = get_messages_content(messages)
# Returns: "USER: Hello\nASSISTANT: Hi!"
```

## System Messages

### `get_system_message(messages)`

Lấy system message.

```python
messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello"},
]
system = get_system_message(messages)
# Returns: {"role": "system", "content": "You are helpful."}
```

### `remove_system_message(messages)`

Xóa system message, trả về list mới.

```python
filtered = remove_system_message(messages)
# Returns: [{"role": "user", "content": "Hello"}]
```

### `pop_system_message(messages)`

Lấy system message và list còn lại.

```python
system, remaining = pop_system_message(messages)
# system = {"role": "system", "content": "You are helpful."}
# remaining = [{"role": "user", "content": "Hello"}]
```

## Thêm/Cập nhật Messages

### `add_or_update_system_message(content, messages, append=False)`

Thêm hoặc cập nhật system message ở đầu list.

```python
messages = [{"role": "user", "content": "Hello"}]

# Thêm system message
messages = add_or_update_system_message("Be helpful", messages)
# Result: [
#     {"role": "system", "content": "Be helpful"},
#     {"role": "user", "content": "Hello"}
# ]

# Cập nhật (append)
messages = add_or_update_system_message("Be concise", messages, append=True)
# Result: [
#     {"role": "system", "content": "Be helpful\nBe concise"},
#     {"role": "user", "content": "Hello"}
# ]
```

### `add_or_update_user_message(content, messages, append=True)`

Thêm hoặc cập nhật user message ở cuối list.

```python
messages = []
messages = add_or_update_user_message("Hello", messages)
# Result: [{"role": "user", "content": "Hello"}]

messages = add_or_update_user_message("How are you?", messages)
# Result: [{"role": "user", "content": "Hello\nHow are you?"}]
```

### `prepend_to_first_user_message_content(content, messages)`

Thêm content vào đầu message user đầu tiên.

```python
messages = [{"role": "user", "content": "What is this?"}]
messages = prepend_to_first_user_message_content("[Context: Python code]\n", messages)
# Result: [{"role": "user", "content": "[Context: Python code]\nWhat is this?"}]
```

### `append_or_update_assistant_message(content, messages)`

Thêm hoặc cập nhật assistant message ở cuối.

```python
messages = [{"role": "user", "content": "Hi"}]
messages = append_or_update_assistant_message("Hello!", messages)
# Result: [
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello!"}
# ]
```

### `update_message_content(message, content, append=True)`

Cập nhật content của message (hỗ trợ multimodal).

```python
msg = {"role": "user", "content": "Hello"}
msg = update_message_content(msg, "World", append=True)
# Returns: {"role": "user", "content": "Hello\nWorld"}

msg = update_message_content(msg, "Start:", append=False)
# Returns: {"role": "user", "content": "Start:\nHello\nWorld"}
```

### `replace_system_message_content(content, messages)`

Thay thế nội dung system message.

```python
messages = [
    {"role": "system", "content": "Old prompt"},
    {"role": "user", "content": "Hi"},
]
messages = replace_system_message_content("New prompt", messages)
# Result: [
#     {"role": "system", "content": "New prompt"},
#     {"role": "user", "content": "Hi"}
# ]
```

## Message Chain

### `get_message_list(messages_map, message_id)`

Xây dựng lại chuỗi messages từ message_id theo parentId.

```python
messages_map = {
    "msg1": {"id": "msg1", "content": "Hi", "parentId": None},
    "msg2": {"id": "msg2", "content": "Hello", "parentId": "msg1"},
    "msg3": {"id": "msg3", "content": "How?", "parentId": "msg2"},
}

chain = get_message_list(messages_map, "msg3")
# Returns: [msg1, msg2, msg3] in order
```

## OpenAI Format Templates

### `openai_chat_chunk_message_template(model, content)`

Tạo SSE chunk theo OpenAI format.

```python
from open_webui.utils.misc import openai_chat_chunk_message_template

chunk = openai_chat_chunk_message_template("gpt-4o", "Hello")
# Returns:
# {
#     "id": "gpt-4o-uuid",
#     "object": "chat.completion.chunk",
#     "created": timestamp,
#     "model": "gpt-4o",
#     "choices": [{
#         "index": 0,
#         "delta": {"content": "Hello"},
#         "logprobs": None,
#         "finish_reason": None
#     }]
# }
```

### `openai_chat_completion_message_template(model, message)`

Tạo completion response theo OpenAI format.

```python
from open_webui.utils.misc import openai_chat_completion_message_template

response = openai_chat_completion_message_template("gpt-4o", "Hello World")
# Returns:
# {
#     "id": "gpt-4o-uuid",
#     "object": "chat.completion",
#     "created": timestamp,
#     "model": "gpt-4o",
#     "choices": [{
#         "index": 0,
#         "message": {"role": "assistant", "content": "Hello World"},
#         "logprobs": None,
#         "finish_reason": "stop"
#     }]
# }
```

## Practical Example

```python
"""
title: Message Modifier Example
"""

try:
    from open_webui.utils.misc import (
        get_last_user_message,
        add_or_update_system_message,
        pop_system_message,
    )
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False


class Filter:
    def __init__(self):
        pass
    
    async def inlet(self, body: dict, __user__: dict = None) -> dict:
        """Modify messages before sending to model"""
        
        messages = body.get("messages", [])
        
        # Get user message
        user_msg = get_last_user_message(messages)
        print(f"User asked: {user_msg}")
        
        # Add/update system prompt
        messages = add_or_update_system_message(
            "You are a helpful assistant. Be concise.",
            messages
        )
        
        body["messages"] = messages
        return body
    
    async def outlet(self, body: dict, __user__: dict = None) -> dict:
        """Process response before sending to user"""
        
        # body contains the response
        return body
```
