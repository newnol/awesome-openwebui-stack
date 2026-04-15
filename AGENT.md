# AGENT.md - Knowledge Base for AI Tool Creation

> **Language note:** The curated catalog (`README.md`, `catalog/`, `categories/`, `stacks/`, contributor docs under `docs/`) is **English-first**. This file remains a detailed Vietnamese reference for tool authoring; for Open WebUI API surface area in English, see `docs/README.md` and related `docs/*.md` files.

---

Tài liệu này cung cấp kiến thức và guidelines để AI có thể tạo ra các công cụ (tools) hiệu quả cho Open WebUI.

---

## Tổng quan về Open WebUI Tools

Open WebUI cho phép tạo các custom tools bằng Python để mở rộng khả năng của AI assistant. Mỗi tool là một Python module có thể được gọi từ chat interface.

### Đặc điểm chính:
- **Async-first**: Các hàm tool phải là async (`async def`)
- **Event-driven**: Hỗ trợ streaming status updates về UI thông qua `EventEmitter`
- **Type-safe**: Sử dụng Pydantic models cho validation
- **User-configurable**: Hỗ trợ `UserValves` để người dùng tùy chỉnh

---

## Cấu trúc chuẩn của một Tool

Mỗi tool Python cho Open WebUI cần tuân theo cấu trúc sau:

### 1. Metadata Header (Docstring)

```python
"""
title: [Tên Tool Hiển Thị]

author: newnol

author_url: https://newnol.io.vn

git_url: https://github.com/newnol/open-webui-tools

description: [Mô tả ngắn gọn về chức năng của tool]

requirements: [package1,package2]  # Các package cần cài đặt

version: 0.1.0

license: MIT
"""
```

### 2. Imports và Dependencies

```python
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
import asyncio
from pydantic import BaseModel, Field
```

### 3. EventEmitter Helper Class

Luôn sử dụng `EventEmitter` để gửi status updates về UI:

```python
class EventEmitter:
    def __init__(self, event_emitter: Callable[[dict], Any] | None = None):
        self.event_emitter = event_emitter

    async def progress_update(self, description: str) -> None:
        await self.emit(description)

    async def error_update(self, description: str) -> None:
        await self.emit(description, "error", True)

    async def success_update(self, description: str) -> None:
        await self.emit(description, "success", True)

    async def emit(
        self,
        description: str = "Unknown State",
        status: str = "in_progress",
        done: bool = False,
    ) -> None:
        if self.event_emitter:
            await self.event_emitter({
                "type": "status",
                "data": {
                    "status": status,
                    "description": description,
                    "done": done,
                },
            })
```

### 4. Tools Class với Valves và UserValves

```python
class Tools:
    class Valves(BaseModel):
        """System-level configuration (không thay đổi bởi user)"""
        CITATION: bool = Field(
            default=True,
            description="True or false for citation (not used yet)."
        )

    class UserValves(BaseModel):
        """User-configurable settings"""
        SETTING_NAME: str = Field(
            default="default_value",
            description="Mô tả setting này làm gì"
        )

    def __init__(self):
        self.valves = self.Valves()
        self.citation = self.valves.CITATION

    async def tool_method_name(
        self,
        param1: str,
        __event_emitter__: Callable[[dict], Any] | None = None,
        __user__: dict = {},
    ) -> str:
        """
        Docstring mô tả tool này làm gì.
        
        :param param1: Mô tả tham số
        :return: Mô tả giá trị trả về
        """
        emitter = EventEmitter(__event_emitter__)
        
        # Initialize user valves nếu chưa có
        if "valves" not in __user__:
            __user__["valves"] = self.UserValves()
        
        try:
            await emitter.progress_update("Bắt đầu xử lý...")
            
            # Validation
            if not param1:
                raise ValueError("Tham số không hợp lệ")
            
            # Xử lý chính (nếu có blocking I/O, dùng asyncio.to_thread)
            result = await asyncio.to_thread(
                blocking_function,
                param1
            )
            
            await emitter.success_update("Hoàn thành!")
            return result
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            await emitter.error_update(error_message)
            return error_message
```

---

## Best Practices

### 1. Error Handling
- **Luôn** wrap logic trong try-except
- **Luôn** gửi error update qua `EventEmitter` trước khi return
- Return error message dạng string để user thấy được

### 2. Async và Blocking Operations
- Nếu có blocking I/O (HTTP requests, file operations), dùng `asyncio.to_thread()`:
```python
result = await asyncio.to_thread(blocking_function, arg1, arg2)
```

### 3. Status Updates
- Gửi `progress_update` khi bắt đầu các bước quan trọng
- Gửi `success_update` khi hoàn thành thành công
- Gửi `error_update` khi có lỗi

### 4. Return Values
- Tool methods **phải return string** (hoặc có thể serialize thành string)
- Nếu cần return structured data, convert sang JSON string hoặc format text dễ đọc

### 5. User Configuration
- Sử dụng `UserValves` cho các settings mà user có thể tùy chỉnh
- Luôn có default values hợp lý
- Validate user input trong tool method

### 6. CLI Testing Support
- Thêm `if __name__ == "__main__":` block để có thể test tool từ command line
- Hữu ích cho debugging và development

### 7. Performance Optimization

Khi làm việc với dữ liệu lớn hoặc operations lặp lại nhiều lần, cần tối ưu hiệu năng:

#### 7.1. Sử dụng Set thay vì List cho Membership Checks

**Tránh:**
```python
available_tools = [
    tool for tool in all_tools if tool["id"] in available_tool_ids  # O(n) lookup
]
```

**Nên dùng:**
```python
available_tool_ids_set = set(available_tool_ids)  # O(1) lookup
available_tools = [
    tool for tool in all_tools if tool["id"] in available_tool_ids_set
]
```

**Lý do:** Set có O(1) average case cho membership check, trong khi list có O(n). Khi có nhiều items, set sẽ nhanh hơn đáng kể.

#### 7.2. Tối ưu List Slicing và Reversing

**Tránh:**
```python
# Đảo toàn bộ list rồi mới lấy 4 phần tử đầu - không hiệu quả
recent_messages = messages[::-1][:4]  # O(n) để reverse toàn bộ list
```

**Nên dùng:**
```python
# Lấy 4 phần tử cuối trước (O(1)), rồi mới reverse (O(k) với k=4)
recent_messages = messages[-4:] if len(messages) >= 4 else messages
reversed_messages = list(reversed(recent_messages))
# Hoặc đơn giản hơn:
reversed_messages = messages[-4:][::-1] if len(messages) >= 4 else messages[::-1]
```

**Lý do:** Chỉ reverse số lượng phần tử cần thiết thay vì reverse toàn bộ list.

#### 7.3. Cải thiện JSON Parsing với Error Handling

**Tránh:**
```python
# Thay tất cả single quotes có thể làm hỏng JSON hợp lệ
content = content.replace("'", '"')
result = json.loads(content)
```

**Nên dùng:**
```python
# Thử parse trước, chỉ thay quotes khi cần thiết
try:
    result = json.loads(content)
except json.JSONDecodeError:
    # Chỉ thay quotes khi parse thất bại
    content = content.replace("'", '"')
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = []  # Fallback value
```

**Lý do:** 
- Giữ nguyên JSON hợp lệ với double quotes
- Chỉ thay đổi khi thực sự cần thiết
- Có fallback để tránh crash

#### 7.4. Caching cho Expensive Operations

Nếu có operations tốn kém được gọi nhiều lần với cùng input:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(input_data: str) -> str:
    # Expensive computation
    return processed_data
```

**Lưu ý:** Chỉ cache các operations:
- Pure functions (không có side effects)
- Có thể hash được input
- Kết quả không thay đổi theo thời gian

#### 7.5. Tránh Unnecessary String Operations

**Tránh:**
```python
# Nối nhiều strings trong loop
result = ""
for item in items:
    result += item  # Tạo string mới mỗi lần
```

**Nên dùng:**
```python
# Sử dụng list comprehension + join
result = "".join(items)
# Hoặc với formatting:
result = "\n".join(f"{i}: {item}" for i, item in enumerate(items))
```

**Lý do:** String concatenation trong loop tạo nhiều temporary objects. `join()` hiệu quả hơn.

---

## Pattern Examples

### Pattern 1: API Integration Tool

```python
async def fetch_api_data(
    self,
    url: str,
    __event_emitter__: Callable[[dict], Any] | None = None,
    __user__: dict = {},
) -> str:
    """
    Fetch data from an external API.
    
    :param url: API endpoint URL
    :return: JSON string or error message
    """
    emitter = EventEmitter(__event_emitter__)
    
    try:
        await emitter.progress_update(f"Fetching data from {url}")
        
        # Blocking HTTP request trong thread
        response = await asyncio.to_thread(
            requests.get,
            url,
            timeout=30
        )
        response.raise_for_status()
        
        await emitter.success_update("Data fetched successfully")
        return json.dumps(response.json(), ensure_ascii=False, indent=2)
        
    except Exception as e:
        error_message = f"Error fetching API: {str(e)}"
        await emitter.error_update(error_message)
        return error_message
```

### Pattern 2: File Processing Tool

```python
async def process_file(
    self,
    file_path: str,
    __event_emitter__: Callable[[dict], Any] | None = None,
    __user__: dict = {},
) -> str:
    """
    Process a file and return results.
    
    :param file_path: Path to the file
    :return: Processed content or error message
    """
    emitter = EventEmitter(__event_emitter__)
    
    try:
        await emitter.progress_update(f"Reading file: {file_path}")
        
        # Blocking file I/O trong thread
        content = await asyncio.to_thread(
            lambda: open(file_path, 'r', encoding='utf-8').read()
        )
        
        # Process content...
        processed = process_content(content)
        
        await emitter.success_update("File processed successfully")
        return processed
        
    except FileNotFoundError:
        error_message = f"File not found: {file_path}"
        await emitter.error_update(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error processing file: {str(e)}"
        await emitter.error_update(error_message)
        return error_message
```

### Pattern 3: Data Transformation Tool

```python
async def transform_data(
    self,
    input_data: str,
    format: str = "json",
    __event_emitter__: Callable[[dict], Any] | None = None,
    __user__: dict = {},
) -> str:
    """
    Transform input data to specified format.
    
    :param input_data: Input data string
    :param format: Output format (json, csv, etc)
    :return: Transformed data string
    """
    emitter = EventEmitter(__event_emitter__)
    
    if "valves" not in __user__:
        __user__["valves"] = self.UserValves()
    
    try:
        await emitter.progress_update(f"Transforming data to {format}")
        
        # Parse input
        parsed = json.loads(input_data)
        
        # Transform based on format
        if format == "csv":
            result = convert_to_csv(parsed)
        else:
            result = json.dumps(parsed, ensure_ascii=False, indent=2)
        
        await emitter.success_update("Transformation complete")
        return result
        
    except json.JSONDecodeError:
        error_message = "Invalid JSON input"
        await emitter.error_update(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error transforming data: {str(e)}"
        await emitter.error_update(error_message)
        return error_message
```

---

## Checklist khi tạo Tool mới

Khi AI tạo một tool mới, cần đảm bảo:

- [ ] **Metadata header** đầy đủ (title, author, description, requirements, version)
- [ ] **EventEmitter** được sử dụng để gửi status updates
- [ ] **Tools class** với Valves và UserValves (nếu cần)
- [ ] **Async method** với signature đúng: `async def method_name(self, params..., __event_emitter__=None, __user__={})`
- [ ] **Error handling** đầy đủ với try-except
- [ ] **Blocking operations** được wrap trong `asyncio.to_thread()`
- [ ] **Return type** là string (hoặc có thể serialize thành string)
- [ ] **Docstring** rõ ràng mô tả parameters và return value
- [ ] **CLI testing** support (optional nhưng recommended)
- [ ] **Dependencies** được liệt kê trong requirements
- [ ] **User configuration** qua UserValves nếu cần thiết
- [ ] **Performance optimization**: Sử dụng set cho membership checks, tối ưu list operations
- [ ] **JSON parsing**: Có error handling tốt, không thay quotes không cần thiết

---

## Ví dụ Reference: youtube_transcript.py

File `tools/youtube_transcript.py` là một ví dụ hoàn chỉnh về cách implement một tool:

### Điểm nổi bật:
1. ✅ Metadata header đầy đủ
2. ✅ EventEmitter class được implement đúng cách
3. ✅ Helper functions (`extract_video_id`, `_fetch_youtube_transcript_structured`) tách biệt logic
4. ✅ Tools class với Valves và UserValves
5. ✅ Async method với proper error handling
6. ✅ Sử dụng `asyncio.to_thread()` cho blocking I/O
7. ✅ CLI testing support
8. ✅ Return string (transcript text) thay vì structured data

### Cấu trúc:
```
- Metadata docstring
- Imports
- Constants (regex patterns)
- EventEmitter class
- Helper functions (sync)
- Tools class:
  - Valves (system config)
  - UserValves (user config)
  - __init__
  - get_youtube_transcript (async entrypoint)
- CLI block (if __name__ == "__main__")
```

---

## Common Pitfalls để tránh

1. **Quên async/await**: Tool methods phải là async
2. **Blocking event loop**: Không gọi blocking I/O trực tiếp, phải dùng `asyncio.to_thread()`
3. **Không gửi status updates**: User sẽ không biết tool đang làm gì
4. **Return structured objects**: Phải return string, không return dict/list trực tiếp
5. **Thiếu error handling**: Luôn wrap trong try-except
6. **Không validate input**: Luôn validate user input trước khi xử lý
7. **Hardcode values**: Sử dụng UserValves cho các giá trị có thể config
8. **Inefficient membership checks**: Dùng `in` với list thay vì set khi có nhiều items
9. **Unnecessary list operations**: Reverse toàn bộ list khi chỉ cần một phần
10. **Poor JSON parsing**: Thay tất cả quotes mà không thử parse trước

---

## Tips cho AI khi tạo Tools

1. **Đọc kỹ yêu cầu**: Hiểu rõ user muốn tool làm gì
2. **Tham khảo youtube_transcript.py**: Đây là template tốt để follow
3. **Tách logic**: Helper functions cho sync operations, async wrapper cho entrypoint
4. **Think about UX**: Status updates giúp user biết tool đang làm gì
5. **Error messages**: Viết error messages rõ ràng, hữu ích
6. **Documentation**: Docstring phải mô tả rõ parameters và return value
7. **Testability**: Thêm CLI block để dễ test và debug
8. **Performance**: Xem xét hiệu năng khi làm việc với dữ liệu lớn, sử dụng set cho membership checks
9. **JSON handling**: Parse JSON một cách thông minh, có fallback và error handling

---

## Resources

- Open WebUI Tools Documentation: https://docs.openwebui.com/tools
- Example tool: `tools/youtube_transcript.py`
- Project structure: Xem `README` và `tools/README.md`

---

## Development Environment

### Python Virtual Environment

Project này sử dụng Python virtual environment tại `.env/`. **Luôn kích hoạt môi trường này trước khi chạy code hoặc cài đặt packages:**

```bash
# Kích hoạt môi trường
source .env/bin/activate

# Kiểm tra Python đang dùng
which python3
# Output: /Users/newnol/Project/Personal-Project/open-webui-tools/.env/bin/python3

# Cài đặt packages
pip install <package_name>

# Deactivate khi xong
deactivate
```

**Lưu ý quan trọng:**
- Không dùng `pip3 install` trực tiếp trên system Python (sẽ gặp lỗi PEP 668)
- Luôn `source .env/bin/activate` trước khi làm việc với project
- Virtual environment đã được cấu hình sẵn trong thư mục `.env/`

### Môi trường Production (Open WebUI)

Máy chạy Open WebUI là **máy ảo Ubuntu** (không phải macOS). Khi cần cài đặt system packages:

**Trên Ubuntu (production):**
```bash
sudo apt-get update
sudo apt-get install -y <package_name>
```

**Nếu Open WebUI chạy trong Docker:**
```bash
# Exec vào container
docker exec -it <container_id> bash

# Cài đặt packages
apt-get update && apt-get install -y <package_name>
pip install <python_package>
```

**Ví dụ cài Graphviz (cần cho diagram_generator tool):**
- Ubuntu: `sudo apt-get install -y graphviz`
- macOS (dev): `brew install graphviz`
- Docker: `apt-get update && apt-get install -y graphviz`

---

## Notes

- Tác giả: newnol (https://newnol.io.vn)
- Repository: https://github.com/newnol/open-webui-tools
- License: MIT

