# Embedding Utilities

Tạo text embeddings trong Open WebUI.

## Import

```python
from open_webui.utils.embeddings import generate_embeddings
```

## `generate_embeddings()`

Hàm tạo embeddings, tự động route đến đúng backend (OpenAI hoặc Ollama).

### Signature

```python
async def generate_embeddings(
    request: Request,
    form_data: dict,
    user: UserModel,
    bypass_filter: bool = False,
) -> dict
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `request` | `Request` | FastAPI Request object |
| `form_data` | `dict` | Request body với model và input |
| `user` | `UserModel` | User object |
| `bypass_filter` | `bool` | Bỏ qua access control |

### Request Body Format

```python
form_data = {
    "model": "text-embedding-3-small",  # Embedding model ID
    "input": "Text to embed",  # String hoặc List[str]
}

# Hoặc batch
form_data = {
    "model": "text-embedding-3-small",
    "input": ["Text 1", "Text 2", "Text 3"],
}
```

### Response Format (OpenAI Compatible)

```python
{
    "object": "list",
    "data": [
        {
            "object": "embedding",
            "index": 0,
            "embedding": [0.123, -0.456, ...]  # Vector
        }
    ],
    "model": "text-embedding-3-small",
    "usage": {
        "prompt_tokens": 10,
        "total_tokens": 10
    }
}
```

## Complete Example

```python
"""
title: Semantic Search Pipe
"""

from pydantic import BaseModel, Field
from typing import Optional, List

try:
    from open_webui.utils.embeddings import generate_embeddings
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False


class Pipe:
    class Valves(BaseModel):
        EMBEDDING_MODEL: str = Field(
            default="text-embedding-3-small",
            description="Embedding model to use"
        )
    
    def __init__(self):
        self.type = "pipe"
        self.id = "semantic_search"
        self.name = "Semantic Search"
        self.valves = self.Valves()
    
    async def get_embedding(
        self,
        text: str,
        request,
        user
    ) -> Optional[List[float]]:
        """Get embedding for a single text."""
        
        if not EMBEDDINGS_AVAILABLE:
            return None
        
        try:
            response = await generate_embeddings(
                request,
                {
                    "model": self.valves.EMBEDDING_MODEL,
                    "input": text,
                },
                user,
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            print(f"Embedding error: {e}")
            return None
    
    async def get_batch_embeddings(
        self,
        texts: List[str],
        request,
        user
    ) -> Optional[List[List[float]]]:
        """Get embeddings for multiple texts."""
        
        if not EMBEDDINGS_AVAILABLE:
            return None
        
        try:
            response = await generate_embeddings(
                request,
                {
                    "model": self.valves.EMBEDDING_MODEL,
                    "input": texts,
                },
                user,
            )
            # Sort by index to maintain order
            sorted_data = sorted(response["data"], key=lambda x: x["index"])
            return [item["embedding"] for item in sorted_data]
        except Exception as e:
            print(f"Batch embedding error: {e}")
            return None
    
    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __request__: Any = None,
        **kwargs
    ):
        # Create user object
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
        
        # Get user message
        messages = body.get("messages", [])
        user_message = messages[-1].get("content", "") if messages else ""
        
        # Get embedding
        embedding = await self.get_embedding(
            user_message,
            __request__,
            user_obj
        )
        
        if embedding:
            return f"Embedding dimension: {len(embedding)}"
        else:
            return "Failed to get embedding"
```

## Alternative: Using LiteLLM

Nếu cần gọi embedding từ external API (không qua Open WebUI models):

```python
import litellm

async def get_external_embedding(text: str, api_base: str, api_key: str):
    """Get embedding from external API using LiteLLM."""
    
    response = await litellm.aembedding(
        model="openai/text-embedding-3-large",
        input=[text],
        api_base=api_base,
        api_key=api_key,
    )
    return response.data[0]["embedding"]


async def get_batch_external_embeddings(
    texts: List[str],
    api_base: str,
    api_key: str
):
    """Get batch embeddings from external API."""
    
    response = await litellm.aembedding(
        model="openai/text-embedding-3-large",
        input=texts,
        api_base=api_base,
        api_key=api_key,
    )
    return [item["embedding"] for item in response.data]
```

## Cosine Similarity

Hàm tính similarity giữa 2 vectors:

```python
import math

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


# With numpy (faster)
import numpy as np

def cosine_similarity_np(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
```

## Semantic Routing Example

```python
async def semantic_route(
    user_message: str,
    routes: List[dict],
    request,
    user
) -> str:
    """
    Route based on semantic similarity.
    
    routes = [
        {"model": "gpt-4o", "utterances": ["complex", "analyze"]},
        {"model": "gpt-3.5", "utterances": ["simple", "quick"]},
    ]
    """
    
    # Get user message embedding
    user_emb = await get_embedding(user_message, request, user)
    if not user_emb:
        return routes[0]["model"]  # Fallback
    
    best_model = None
    best_score = 0.0
    
    for route in routes:
        # Get embeddings for route utterances
        route_embs = await get_batch_embeddings(
            route["utterances"],
            request,
            user
        )
        
        if not route_embs:
            continue
        
        # Find max similarity
        for emb in route_embs:
            score = cosine_similarity(user_emb, emb)
            if score > best_score:
                best_score = score
                best_model = route["model"]
    
    return best_model or routes[0]["model"]
```
