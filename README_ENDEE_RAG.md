# Endee RAG System - Complete Implementation

A production-ready AI-powered Retrieval-Augmented Generation (RAG) system using Endee vector database and OpenAI GPT-4o-mini for semantic search and answer generation.

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [How to Run](#how-to-run)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Example Usage](#example-usage)
- [Troubleshooting](#troubleshooting)

## Project Overview

The Endee RAG System is a complete AI application that demonstrates how to use Endee vector database for semantic search combined with OpenAI's LLMs for intelligent answer generation.

### What It Does

1. **Ingests Documents**: Loads .txt, .pdf, and .md files
2. **Generates Embeddings**: Creates vector embeddings using OpenAI's text-embedding-3-small
3. **Stores in Endee**: Stores vectors in Endee vector database
4. **Semantic Search**: Retrieves relevant documents using vector similarity
5. **Generates Answers**: Uses GPT-4o-mini to generate contextual answers

### Problem It Solves

- Find information in large document collections instantly
- Get AI-powered answers based on your specific documents
- Combine structured data retrieval with generative AI
- Maintain conversation context with document references

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 User Interface Layer                    │
│  Streamlit Web App | REST API | Command Line Tools     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              FastAPI Backend (app.py)                    │
│  - Document Upload & Ingestion                          │
│  - Query Processing                                     │
│  - Response Streaming                                   │
└────────────────────┬────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼──────────┐  ┌─▼────────────┐  ┌▼──────────────┐
│   Document   │  │  RAG System  │  │  Analytics &  │
│  Processor   │  │  Pipeline    │  │   Caching     │
│              │  │              │  │               │
│ - Parse      │  │ - Retrieve   │  │ - Query Cache │
│ - Chunk      │  │ - Generate   │  │ - Metrics     │
│ - Clean      │  │ - Stream     │  │ - Logging     │
└──────────────┘  └──────────────┘  └───────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼──────────┐  ┌─▼────────────┐  │
│   OpenAI     │  │    Endee     │  │
│   Client     │  │  Vector DB   │  │
│              │  │              │  │
│ - Embed      │  │ - Store      │  │
│ - Complete   │  │ - Search     │  │
│ - Stream     │  │ - Retrieve   │  │
└──────────────┘  └──────────────┘  │
                                     │
                          (Vector Storage)
```

### Workflow

```
User Query
    ↓
[Document Processor] ← Load .txt, .pdf, .md files
    ↓
[Text Chunking] ← Split into manageable pieces
    ↓
[Embedding Generation] ← OpenAI text-embedding-3-small
    ↓
[Endee Vector DB] ← Store embeddings + metadata
    ↓
[Semantic Search] ← Query embedding → Find similar docs
    ↓
[Context Retrieval] ← Get top-K relevant chunks
    ↓
[LLM Response] ← GPT-4o-mini generates answer
    ↓
[Stream/Return] ← Real-time or complete response
```

## Features

### Core Features

- **Document Processing**
  - Support for .txt, .pdf, .md files
  - Intelligent text chunking with overlap
  - Automatic metadata extraction
  - Batch document processing

- **Vector Database Integration**
  - Full Endee HTTP client implementation
  - Batch vector operations
  - Semantic similarity search
  - Vector metadata management
  - Health checks and stats

- **OpenAI Integration**
  - Embedding generation (text-embedding-3-small)
  - LLM completions (GPT-4o-mini)
  - Batch embeddings support
  - Async/sync operations
  - Token usage tracking

- **RAG Pipeline**
  - Complete semantic search workflow
  - Context-aware answer generation
  - Source attribution
  - Streaming responses
  - Performance metrics

### Web Interface (Streamlit)

- Chat interface with conversation history
- Document upload and management
- Semantic search exploration
- Real-time analytics dashboard
- System configuration and management

### REST API (FastAPI)

- 9+ production-ready endpoints
- Streaming support
- Health checks
- Comprehensive error handling
- OpenAPI/Swagger documentation

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API key
- Endee vector database server running

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment Variables

Create a `.env` file:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here

# Endee Configuration
ENDEE_HOST=localhost
ENDEE_PORT=8000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Streamlit Configuration
STREAMLIT_PORT=8501
```

### Step 3: Start Endee Vector Database

```bash
# Docker (recommended)
docker run -p 8000:8000 endeeio/endee:latest

# Or from source
cd endee-master
./run.sh
```

### Step 4: Verify Setup

```bash
python scripts/verify_setup.py
```

## Quick Start

### 5-Minute Setup

1. **Get API Keys**
   ```bash
   # Get OpenAI API key from https://platform.openai.com/api-keys
   export OPENAI_API_KEY="sk-..."
   ```

2. **Start Endee**
   ```bash
   docker run -p 8000:8000 endeeio/endee:latest
   ```

3. **Start Backend API**
   ```bash
   python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
   ```

4. **Start Web UI**
   ```bash
   streamlit run frontend/app.py
   ```

5. **Access**
   - Web UI: http://localhost:8501
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## How to Run

### Option 1: Using Startup Script

```bash
./start.sh
```

This will:
- Start Endee database
- Start FastAPI backend
- Start Streamlit frontend
- Open browser to UI

### Option 2: Docker Compose

```bash
docker-compose -f docker-compose-app.yml up
```

### Option 3: Manual Startup

**Terminal 1 - Endee Database:**
```bash
docker run -p 8000:8000 endeeio/endee:latest
```

**Terminal 2 - API Backend:**
```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 3 - Streamlit Web:**
```bash
streamlit run frontend/app.py
```

### Option 4: Jupyter Notebooks

```bash
jupyter notebook
# Open notebooks/demo.ipynb
```

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "endee_connected": true,
  "openai_configured": true,
  "rag_ready": true
}
```

#### 2. Ask Question
```bash
POST /ask

{
  "question": "What is machine learning?",
  "top_k": 5,
  "min_score": 0.3
}
```

Response:
```json
{
  "query": "What is machine learning?",
  "answer": "Machine learning is...",
  "retrieved_documents": [...],
  "retrieval_score": 0.75,
  "response_time_ms": 2500,
  "tokens_used": 1250
}
```

#### 3. Semantic Search
```bash
POST /search

{
  "question": "machine learning definition",
  "top_k": 5,
  "min_score": 0.3
}
```

#### 4. Upload Document
```bash
POST /upload
Content-Type: multipart/form-data

file: [binary file content]
```

#### 5. Ingest Documents
```bash
POST /ingest

{
  "file_paths": ["/path/to/doc1.txt", "/path/to/doc2.pdf"],
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

#### 6. Stream Response
```bash
POST /stream

{
  "question": "What is AI?",
  "top_k": 5
}
```

Returns: Server-sent events (SSE) stream

#### 7. Get Statistics
```bash
GET /stats
```

#### 8. Optimize Query
```bash
POST /optimize-query

{
  "query": "tell me about machine learning please"
}
```

#### 9. Vector Database Stats
```bash
GET /vectors/stats
```

### Full API Documentation

Visit: http://localhost:8000/docs (Swagger UI)
Visit: http://localhost:8000/redoc (ReDoc)

## Configuration

### Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=sk-...              # Required: Your OpenAI API key

# Endee
ENDEE_HOST=localhost               # Endee server host
ENDEE_PORT=8000                    # Endee server port

# API Server
API_HOST=0.0.0.0                   # API bind address
API_PORT=8000                      # API port

# Logging
LOG_LEVEL=INFO                     # Log level
```

### Document Processing

Edit `backend/document_processor.py`:

```python
processor = DocumentProcessor(
    chunk_size=500,          # Words per chunk
    chunk_overlap=50,        # Overlap between chunks
    min_chunk_size=100       # Minimum chunk size
)
```

### RAG System

Edit `backend/rag_system.py`:

```python
rag_system = RAGSystem(
    endee_db=endee_db,
    openai_client=openai_client,
    top_k=5,                 # Number of results to retrieve
    min_score=0.3            # Minimum similarity score
)
```

## Project Structure

```
endee-rag/
├── backend/
│   ├── app.py                      # FastAPI application
│   ├── endee_vector_db.py          # Endee vector DB client
│   ├── openai_client.py            # OpenAI integration
│   ├── document_processor.py       # Document loading & chunking
│   ├── rag_system.py               # RAG pipeline
│   ├── analytics.py                # Analytics & monitoring
│   ├── cache_manager.py            # Query caching
│   └── __init__.py
│
├── frontend/
│   ├── app.py                      # Streamlit web interface
│   └── requirements-ui.txt
│
├── scripts/
│   ├── ingest_documents.py         # Document ingestion script
│   ├── test_api.py                 # API testing
│   ├── verify_setup.py             # Setup verification
│   └── demo.py                     # Interactive demo
│
├── notebooks/
│   ├── demo.ipynb                  # Jupyter demo notebook
│   └── analysis.ipynb              # Analysis notebook
│
├── config.yaml                     # Configuration spec
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── Dockerfile                      # Container image
├── docker-compose-app.yml          # Multi-service compose
├── start.sh                        # Startup script
│
├── README_ENDEE_RAG.md             # This file
├── SETUP_GUIDE.md                  # Detailed setup
├── API_REFERENCE.md                # API documentation
└── TROUBLESHOOTING.md              # Troubleshooting guide
```

## Example Usage

### 1. Using Python SDK

```python
import asyncio
from backend.endee_vector_db import get_endee_client
from backend.openai_client import get_openai_client
from backend.rag_system import get_rag_system

async def main():
    # Initialize clients
    endee_db = await get_endee_client()
    openai_client = get_openai_client()
    rag_system = await get_rag_system(endee_db, openai_client)
    
    # Ingest documents
    result = await rag_system.ingest_documents([
        "documents/guide.txt",
        "documents/manual.pdf"
    ])
    print(f"Ingested: {result}")
    
    # Ask question
    response = await rag_system.answer_question("What is included in the guide?")
    print(f"Answer: {response.answer}")
    print(f"Sources: {len(response.retrieved_documents)}")

asyncio.run(main())
```

### 2. Using REST API

```bash
# Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "top_k": 5
  }'

# Search documents
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "question": "key information",
    "top_k": 3
  }'
```

### 3. Using Streamlit UI

```bash
streamlit run frontend/app.py
```

Then:
1. Go to "Document Upload" tab
2. Upload documents
3. Go to "Chat" tab
4. Ask questions
5. View analytics in "Analytics" tab

## Troubleshooting

### Endee Connection Issues

```bash
# Check if Endee is running
curl http://localhost:8000/health

# View Endee logs
docker logs <container-id>

# Restart Endee
docker restart <container-id>
```

### OpenAI API Errors

```
"Error: Incorrect API key provided"
→ Check OPENAI_API_KEY in .env file

"Error: Rate limit exceeded"
→ Wait a few minutes before retrying

"Error: Insufficient quota"
→ Check your OpenAI account credits
```

### Backend Connection Issues

```
"Cannot connect to API server"
→ Make sure backend is running: python -m uvicorn backend.app:app

"Port already in use"
→ Change port: uvicorn backend.app:app --port 8001
```

### Streamlit Issues

```
"Failed to connect to FastAPI"
→ Verify API_BASE_URL in frontend/app.py matches your setup

"Slow performance"
→ Reduce chunk_size or top_k in RAG system config
```

## Performance Optimization

### For Large Document Collections

```python
# Increase batch size for embeddings
texts = [...]
results = openai_client.generate_embeddings_batch(texts)

# Use filtering to reduce search space
results = await endee_db.search(
    query_embedding=emb,
    top_k=3,
    metadata_filter={"file_type": "pdf"}
)
```

### For Real-Time Responses

```python
# Use streaming
async for chunk in rag_system.stream_answer(query):
    # Update UI in real-time
    pass

# Cache frequently asked questions
cache.set(query, response)
```

## Advanced Features

### Custom Prompts

```python
custom_prompt = """You are a helpful assistant specialized in legal documents.
Always cite the specific section when referencing information."""

response = await rag_system.generate_response(
    query=question,
    context=context,
    system_prompt=custom_prompt
)
```

### Metadata Filtering

```python
results = await endee_db.search(
    query_embedding=embedding,
    metadata_filter={"source": "contracts", "year": 2024}
)
```

### Batch Processing

```python
from backend.document_processor import process_documents_batch

chunks = process_documents_batch(
    file_paths=["doc1.txt", "doc2.pdf", "doc3.md"],
    chunk_size=500,
    chunk_overlap=50
)
```

## License

MIT License - See LICENSE file for details

## Support

- GitHub: https://github.com/endee-io/endee
- Documentation: https://docs.endee.io
- Issues: https://github.com/endee-io/endee/issues

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Changelog

### v1.0.0 (2024)
- Initial release
- Full Endee integration
- OpenAI GPT-4o-mini support
- Streamlit web interface
- REST API with 9 endpoints
- Document processing pipeline
- Semantic search implementation
