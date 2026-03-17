# Complete API Reference Guide

## Overview

The Endee RAG System provides a comprehensive REST API for all operations. Base URL: `http://localhost:8000`

Interactive documentation available at: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently no authentication required for local development.

For production, implement:
```python
# backend/app.py
from fastapi.security import HTTPBearer
security = HTTPBearer()
```

## Document Endpoints

### Upload Document
```http
POST /api/documents/upload
Content-Type: multipart/form-data

file: <PDF|TXT|MD file>
```

Response:
```json
{
  "success": true,
  "data": {
    "document_id": "doc_123",
    "filename": "document.pdf",
    "chunks": 45,
    "vectors_stored": 45,
    "processing_time": 3.2
  }
}
```

### List Documents
```http
GET /api/documents/list
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "doc_123",
      "filename": "document.pdf",
      "size": 1024000,
      "chunks": 45,
      "uploaded_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Document
```http
GET /api/documents/{doc_id}
```

### Delete Document
```http
DELETE /api/documents/{doc_id}
```

## Query Endpoints

### Ask Question
```http
POST /api/query/ask
Content-Type: application/json

{
  "question": "What is machine learning?",
  "top_k": 5,
  "min_score": 0.5
}
```

Response:
```json
{
  "success": true,
  "data": {
    "answer": "Machine learning is...",
    "sources": [
      {
        "document": "ml_guide.pdf",
        "chunk_id": "chunk_5",
        "text": "Machine learning is a subset of...",
        "score": 0.95
      }
    ],
    "confidence": 0.92
  },
  "metadata": {
    "response_time": 2.3,
    "tokens_used": 450
  }
}
```

### Stream Response
```http
POST /api/query/stream
Content-Type: application/json

{
  "question": "Explain quantum computing"
}
```

Returns streaming response with token-by-token generation.

### Semantic Search
```http
POST /api/search
Content-Type: application/json

{
  "query": "important information",
  "top_k": 10,
  "min_score": 0.5
}
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "document": "document.pdf",
      "chunk_id": "chunk_1",
      "text": "...",
      "score": 0.98,
      "position": 0
    }
  ]
}
```

### Optimize Query
```http
POST /api/query/optimize
Content-Type: application/json

{
  "question": "what is machine learning and how does it work"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "original": "what is machine learning and how does it work",
    "optimized": "machine learning definition and mechanisms",
    "keywords": ["machine learning", "definition", "mechanisms"],
    "query_type": "definition_and_explanation"
  }
}
```

## System Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "services": {
    "endee": "connected",
    "openai": "connected",
    "cache": "operational"
  }
}
```

### System Statistics
```http
GET /api/stats
```

Response:
```json
{
  "success": true,
  "data": {
    "total_documents": 5,
    "total_vectors": 243,
    "cache_size": 50,
    "cache_hit_rate": 0.65,
    "total_queries": 156,
    "avg_response_time": 2.3,
    "success_rate": 0.95,
    "last_update": "2024-01-15T11:30:00Z"
  }
}
```

### Cache Statistics
```http
GET /api/cache/stats
```

Response:
```json
{
  "success": true,
  "data": {
    "total_cached": 50,
    "cache_size_mb": 2.3,
    "hit_rate": 0.65,
    "miss_rate": 0.35,
    "avg_cache_age": 3600,
    "ttl_seconds": 7200
  }
}
```

### Clear Cache
```http
POST /api/cache/clear
```

Response:
```json
{
  "success": true,
  "data": {
    "cleared": 50,
    "message": "Cache cleared successfully"
  }
}
```

## Error Responses

All errors follow standard format:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Question cannot be empty",
    "details": {}
  }
}
```

### Common Errors

| Code | Status | Meaning |
|------|--------|---------|
| INVALID_REQUEST | 400 | Missing or invalid parameters |
| NOT_FOUND | 404 | Document or resource not found |
| SERVICE_ERROR | 503 | Endee or OpenAI unavailable |
| RATE_LIMITED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |

## Rate Limiting

Local development: No limits

Production (recommended):
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/query/ask")
@limiter.limit("10/minute")
async def ask_question(request):
    pass
```

## Example Implementations

### Python Client
```python
import requests

class EndeeClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def ask(self, question, top_k=5):
        response = requests.post(
            f"{self.base_url}/api/query/ask",
            json={"question": question, "top_k": top_k}
        )
        return response.json()
    
    def search(self, query, top_k=10):
        response = requests.post(
            f"{self.base_url}/api/search",
            json={"query": query, "top_k": top_k}
        )
        return response.json()

# Usage
client = EndeeClient()
result = client.ask("What is machine learning?")
print(result["data"]["answer"])
```

### JavaScript/Node.js Client
```javascript
class EndeeClient {
  constructor(baseUrl = "http://localhost:8000") {
    this.baseUrl = baseUrl;
  }
  
  async ask(question, topK = 5) {
    const response = await fetch(`${this.baseUrl}/api/query/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, top_k: topK })
    });
    return await response.json();
  }
  
  async search(query, topK = 10) {
    const response = await fetch(`${this.baseUrl}/api/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: topK })
    });
    return await response.json();
  }
}

// Usage
const client = new EndeeClient();
const result = await client.ask("What is machine learning?");
console.log(result.data.answer);
```

### cURL Examples

**Ask Question**
```bash
curl -X POST http://localhost:8000/api/query/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is artificial intelligence?"}'
```

**Upload Document**
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@document.pdf"
```

**Search**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "important topic", "top_k": 10}'
```

## Rate Limits & Best Practices

1. **Batch Queries** - Send multiple questions together
2. **Use Caching** - Leverage cached results for similar questions
3. **Optimal Top-K** - Start with 5, increase if needed
4. **Document Size** - Keep files under 100MB
5. **Concurrent Requests** - Max 10 parallel requests per second

## Webhooks (Coming Soon)

Subscribe to events:
```bash
POST /api/webhooks/subscribe
{
  "event": "query_completed",
  "url": "https://your-domain.com/webhook"
}
```

Events:
- `query_completed` - After answer generated
- `document_uploaded` - After document processed
- `cache_hit` - When cached result used

## Versioning

Current API version: `v1`

Future versions will be backwards compatible or available at `/api/v2/`
