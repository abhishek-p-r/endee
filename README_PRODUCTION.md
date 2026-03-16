# Endee AI Knowledge Assistant - Production Implementation

**A Complete RAG-Powered Knowledge Assistant using Endee Vector Database and OpenAI**

## 🎯 Project Overview

This is a **production-ready AI knowledge assistant** that combines:

- **Endee Vector Database** - For fast semantic search over embeddings
- **OpenAI Embeddings** - For high-quality text embeddings (text-embedding-3-small)
- **OpenAI GPT** - For intelligent answer generation
- **FastAPI** - For RESTful backend API
- **Streamlit** - For interactive web frontend

The system implements **Retrieval Augmented Generation (RAG)** to answer questions based on a knowledge base of documents.

## ⚙️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                    │
│                   Streamlit Web Interface                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FASTAPI BACKEND                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Endpoints:                                           │   │
│  │ - /query          → Full RAG pipeline               │   │
│  │ - /query/retrieve → Search only                     │   │
│  │ - /query/stream   → Streaming responses             │   │
│  │ - /documents/upload → Process documents             │   │
│  │ - /health         → System status                   │   │
│  │ - /stats          → Collection statistics            │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────────┐  ┌──────────────┐  ┌─────────────┐
    │   OpenAI   │  │    Endee     │  │  Document   │
    │Embeddings  │  │   Vector DB  │  │ Processor   │
    └────────────┘  └──────────────┘  └─────────────┘
```

## 🔄 Query Processing Workflow

```
1. USER QUERY
   ↓
2. EMBEDDING GENERATION
   - Convert query to vector using OpenAI
   - Create 1536-dimensional embedding
   ↓
3. SEMANTIC SEARCH IN ENDEE
   - Search Endee vector database
   - Find top K most similar documents
   - Use cosine similarity scoring
   ↓
4. CONTEXT RETRIEVAL
   - Extract relevant text chunks
   - Gather metadata and sources
   ↓
5. PROMPT CONSTRUCTION
   - Create RAG prompt with context
   - Include retrieved documents
   ↓
6. ANSWER GENERATION
   - Send prompt to GPT-3.5-turbo
   - Generate contextual answer
   ↓
7. RESPONSE
   - Return answer with metadata
   - Include source attribution
   - Provide performance metrics
```

## 📦 How Endee is Used

### Vector Storage
- Documents are **chunked** into overlapping segments (512 characters)
- Each chunk is **embedded** using OpenAI embeddings (1536 dimensions)
- Vectors are **stored in Endee** with rich metadata

### Metadata Storage
Each vector in Endee includes:
```json
{
  "document_id": "doc_abc123",
  "chunk_id": "chunk_123",
  "text": "The actual chunk content...",
  "source": "/path/to/document.pdf",
  "chunk_index": 0,
  "total_chunks": 5,
  "created_at": "2024-01-20T10:30:00",
  "metadata": {
    "document_name": "Example Document",
    "file_type": "pdf",
    "char_count": 512
  }
}
```

### Semantic Search in Endee
- User query → embedded as vector (1536 dimensions)
- **Cosine similarity search** in Endee
- **Top K results** with scores (0-1)
- **Score threshold** filtering (default 0.5)

### Performance
- **Search time**: 100-500ms for typical queries
- **Embedding time**: 200-1000ms depending on text size
- **Answer generation**: 2-5 seconds

## 📁 Project Structure

```
project/
├── backend_v2/                      # Backend implementation
│   ├── main.py                      # FastAPI application (478 lines)
│   ├── endee_integration.py         # Endee vector DB client (330 lines)
│   ├── openai_embeddings.py         # OpenAI embeddings service (213 lines)
│   ├── document_processor.py        # Document loading & chunking (341 lines)
│   ├── rag_pipeline.py              # RAG pipeline (387 lines)
│   ├── ingest_documents.py          # Batch document ingestion (236 lines)
│   └── __init__.py
│
├── frontend_v2/                     # Frontend implementation
│   └── app.py                       # Streamlit web interface (536 lines)
│
├── scripts/
│   ├── setup.sh                     # Setup script
│   ├── start_backend.sh             # Start FastAPI server
│   └── start_frontend.sh            # Start Streamlit app
│
├── data/                            # Documents to ingest
│   ├── *.txt                        # Text files
│   ├── *.pdf                        # PDF files
│   └── *.md                         # Markdown files
│
├── uploads/                         # User-uploaded documents
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── docker-compose.yml               # Docker orchestration
└── README_PRODUCTION.md             # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10+
- Endee server running (or Docker)
- OpenAI API key
- pip or conda

### Step 1: Clone Repository

```bash
git clone https://github.com/abhishek-p-r/endee.git
cd endee
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here

# Endee Configuration
ENDEE_URL=http://localhost:6379
ENDEE_DB_NAME=knowledge_base

# Server Configuration
API_URL=http://localhost:8000
PORT=8000
HOST=0.0.0.0

# Data
DATA_DIR=./data
```

### Step 5: Start Endee Server

**Option A: Using Docker** (Recommended)

```bash
docker run -p 6379:6379 endeeio/endee:latest
```

**Option B: Local Installation**

See [Endee GitHub](https://github.com/endee-io/endee) for local setup.

### Step 6: Ingest Documents

```bash
# Create data directory
mkdir -p data
# Place your .txt, .pdf, .md files in the data/ directory

# Run ingestion
cd backend_v2
python ingest_documents.py
```

Example output:
```
INFO - Found 5 documents
INFO - Processing: document1.txt
INFO - Created 10 chunks
INFO - Stored 10 vectors in Endee
...
==================================================
INGESTION REPORT
==================================================
Status: ✓ Success
Documents Ingested: 5
Failed: 0
Collection Stats: {count: 150, memory_used_mb: 25}
==================================================
```

## ▶️ Running the Application

### Option 1: Automated (Docker Compose)

```bash
docker-compose up
```

Then:
- **API**: http://localhost:8000/docs
- **Frontend**: http://localhost:8501
- **Endee**: http://localhost:6379

### Option 2: Manual - Start Backend

```bash
cd backend_v2
python main.py
```

Output:
```
INFO - Starting FastAPI server on 0.0.0.0:8000
INFO - Uvicorn running on http://0.0.0.0:8000
INFO - Endee connection established
INFO - RAG pipeline initialized
```

API available at: **http://localhost:8000/docs**

### Option 3: Manual - Start Frontend

```bash
cd frontend_v2
streamlit run app.py
```

Access at: **http://localhost:8501**

### Option 4: Both Services

```bash
# Terminal 1
cd backend_v2 && python main.py

# Terminal 2
cd frontend_v2 && streamlit run app.py
```

## 📚 API Reference

### Full API Documentation

Once backend is running, access at: `http://localhost:8000/docs`

### Key Endpoints

#### Query Endpoint (Full RAG)

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is semantic search?",
    "top_k": 5,
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

Response:
```json
{
  "query": "What is semantic search?",
  "answer": "Semantic search is a search technique that...",
  "context_chunks": [
    {
      "id": "chunk_123",
      "score": 0.89,
      "text": "Semantic search refers to...",
      "source": "/data/document.txt"
    }
  ],
  "sources": ["/data/document.txt"],
  "retrieval_time": 0.234,
  "generation_time": 2.156,
  "success": true
}
```

#### Retrieval Only Endpoint

```bash
curl -X POST http://localhost:8000/query/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your question here",
    "top_k": 5
  }'
```

#### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "endee_connected": true,
  "timestamp": "2024-01-20T10:30:00"
}
```

#### Collection Statistics

```bash
curl http://localhost:8000/stats
```

#### Document Upload

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@document.pdf"
```

## 🧪 Testing the System

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

Expected: `"status": "healthy"`

### Test 2: Simple Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What documents do I have?"}'
```

Expected: Answer based on your documents

### Test 3: Semantic Search Only

```bash
curl -X POST http://localhost:8000/query/retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "important topic", "top_k": 3}'
```

Expected: List of relevant chunks with scores

## 💡 Usage Examples

### Example 1: Question Answering

**Query**: "What are the main benefits of AI?"

**System Response**:
1. Converts query to embedding
2. Searches Endee for similar documents
3. Retrieves top 5 relevant chunks
4. Generates answer with context
5. Returns answer + sources + metrics

### Example 2: Document Upload & Query

```bash
# Upload document
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@my_research.pdf"

# After processing (5-30 seconds)

# Ask question about it
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the findings?"}'
```

### Example 3: Streamlit UI

1. Open http://localhost:8501
2. Go to "Chat" tab
3. Type your question
4. System searches documents and generates answer
5. View sources and metrics

## 🔍 Monitoring & Debugging

### Check Endee Connection

```bash
curl http://localhost:6379/health
```

### View Collection Stats

```bash
curl http://localhost:8000/stats
```

### Enable Debug Logging

Set in `.env`:
```env
LOG_LEVEL=DEBUG
```

### Check API Health

```bash
curl http://localhost:8000/health
```

## ⚙️ Configuration Guide

### OpenAI Models

**For Embeddings**:
- `text-embedding-3-small` (default) - 1536 dimensions, best value
- `text-embedding-3-large` - 3072 dimensions, higher quality

**For Generation**:
- `gpt-3.5-turbo` (default) - Fast, good quality
- `gpt-4` - More capable, slower, more expensive

### Chunking Parameters

In `backend_v2/document_processor.py`:
```python
processor = DocumentProcessor(
    chunk_size=512,      # Characters per chunk
    chunk_overlap=50     # Overlap between chunks
)
```

### Search Parameters

In API requests:
```json
{
  "top_k": 5,              # Number of results
  "score_threshold": 0.5,  # Minimum similarity (0-1)
  "temperature": 0.7,      # Answer creativity (0-1)
  "max_tokens": 1000       # Answer length limit
}
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t endee-assistant .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Access Services

- API: http://localhost:8000
- Frontend: http://localhost:8501
- Endee: http://localhost:6379

### View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📊 Performance Metrics

### Typical Response Times

| Operation | Time |
|-----------|------|
| Query Embedding | 200-500ms |
| Endee Search (5 results) | 100-300ms |
| GPT Answer Generation | 2-5s |
| **Total** | **2.3-5.8s** |

### Optimization Tips

1. **Reduce top_k**: Fewer results = faster search
2. **Increase chunk_size**: Fewer chunks to embed
3. **Use smaller model**: `text-embedding-3-small` vs large
4. **Enable caching**: Cache frequent queries
5. **Batch embeddings**: Process multiple at once

## 🔐 Security Considerations

### API Security
- [ ] Add API key authentication
- [ ] Implement rate limiting
- [ ] Use HTTPS in production
- [ ] Validate all inputs

### Data Security
- [ ] Encrypt sensitive documents
- [ ] Use secure storage for embeddings
- [ ] Implement access controls
- [ ] Log sensitive operations

### OpenAI API
- [ ] Keep API key secret (use .env)
- [ ] Use least privilege key
- [ ] Monitor usage/costs
- [ ] Implement quotas

## 📝 Code Structure

### Backend Modules

**endee_integration.py** (330 lines)
- EndeeVectorDB class
- Connection management
- Storage and search operations
- Collection management

**openai_embeddings.py** (213 lines)
- OpenAIEmbeddingService class
- Text embedding generation
- Batch processing
- Async support

**document_processor.py** (341 lines)
- Document loading (TXT, PDF, MD)
- Text chunking
- Metadata extraction
- Directory processing

**rag_pipeline.py** (387 lines)
- RAGPipeline class
- Context retrieval
- Prompt engineering
- Answer generation
- Streaming support

**main.py** (478 lines)
- FastAPI application
- All endpoints (8+)
- Request/response models
- Error handling
- CORS configuration

### Frontend (536 lines)

**app.py**
- Streamlit interface
- Chat UI with history
- Semantic search interface
- Analytics dashboard
- Document upload
- System monitoring

## 🧹 Cleanup & Maintenance

### Clear Collection

```bash
curl -X DELETE http://localhost:8000/collections/knowledge_base
```

### Reset Database

```bash
# Stop services
docker-compose down

# Remove volumes
docker volume rm endee_vol

# Restart
docker-compose up
```

### Delete Uploads

```bash
rm -rf uploads/*
```

## 📖 Additional Resources

- [Endee GitHub](https://github.com/endee-io/endee)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Streamlit Docs](https://docs.streamlit.io)

## 🚨 Troubleshooting

### Endee Connection Error

```
Error: Connection refused at localhost:6379
```

**Solution**: Start Endee server first
```bash
docker run -p 6379:6379 endeeio/endee:latest
```

### OpenAI API Error

```
Error: Invalid API key
```

**Solution**: Check .env file has valid OPENAI_API_KEY

### Empty Search Results

- Check documents were ingested successfully
- Verify Endee has vectors: `curl http://localhost:8000/stats`
- Try adjusting `score_threshold`

### Slow Responses

- Reduce `top_k` parameter
- Check API rate limits
- Verify network latency
- Profile with debug logging

## 📄 License

This project uses:
- Endee: Custom License
- OpenAI: Commercial License
- FastAPI: MIT License
- Streamlit: Apache 2.0 License

## 🎯 Next Steps

1. ✅ Set up the system (follow installation)
2. ✅ Add your documents (place in data/ folder)
3. ✅ Run ingestion (python ingest_documents.py)
4. ✅ Start application (docker-compose up)
5. ✅ Ask questions (http://localhost:8501)

## 📞 Support

For issues:
1. Check troubleshooting section
2. View logs: `docker-compose logs`
3. Check API health: `curl http://localhost:8000/health`
4. Review Endee status: `curl http://localhost:6379/health`

## ✨ Key Features Summary

✅ **Production Ready**: Full error handling, logging, monitoring
✅ **Endee Integration**: Proper vector storage and search
✅ **OpenAI Powered**: GPT-3.5-turbo for answers
✅ **RAG Architecture**: Context-aware generation
✅ **Multiple Formats**: Support TXT, PDF, Markdown
✅ **REST API**: FastAPI with Swagger docs
✅ **Web UI**: Interactive Streamlit interface
✅ **Performance**: Real-time metrics and monitoring
✅ **Scalable**: Async operations throughout
✅ **Well Documented**: Comprehensive README

---

**Built with ❤️ using Endee Vector Database & OpenAI GPT**

Last Updated: January 2024
