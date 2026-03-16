# Endee AI Knowledge Assistant - Retrieval Augmented Generation (RAG) System

A production-ready Retrieval Augmented Generation (RAG) application using **Endee Vector Database** for semantic search and Google Gemini AI for intelligent response generation. This project demonstrates a complete AI application that loads documents, generates embeddings, stores them in Endee, and retrieves relevant information to answer user questions.

## Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [How Endee is Used](#how-endee-is-used)
- [Installation and Setup](#installation-and-setup)
- [How to Run](#how-to-run)
- [Example Usage](#example-usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

This AI Knowledge Assistant demonstrates a **complete production-ready RAG system** using Endee as the primary vector database. The system:

- **Loads documents** from `.txt` files
- **Generates embeddings** using SentenceTransformers
- **Stores vectors** in Endee vector database with metadata
- **Performs semantic search** to retrieve relevant documents
- **Generates answers** using Google Gemini AI
- **Maintains conversation** history and context

### Key Features

✅ Multi-agent RAG pipeline (4 specialized bots)
✅ Endee vector database integration for semantic search
✅ Document ingestion from `.txt` files
✅ Embeddings using sentence-transformers (384 dimensions)
✅ FastAPI backend with 14+ endpoints
✅ Streamlit web UI for easy interaction
✅ Conversation memory management
✅ Query optimization and caching
✅ Real-time analytics dashboard
✅ Production-ready with logging and error handling

---

## System Architecture

### Complete Data Flow

```
USER QUESTION
    ↓
[Query Understanding Bot]
    - Optimize query
    - Detect intent
    - Extract keywords
    ↓
[Generate Query Embedding]
    - Convert to 384-dim vector
    - Using SentenceTransformers
    ↓
[ENDEE VECTOR DATABASE]
    ┌─────────────────────────────┐
    │ Collections & Vectors       │
    │ ├─ Metadata filtering       │
    │ ├─ Cosine similarity search │
    │ └─ Top-K retrieval          │
    └─────────────────────────────┘
    ↓
[Retrieve Relevant Documents]
    - Top 5 similar chunks
    - With metadata and scores
    ↓
[Knowledge Retrieval Bot]
    - Format context
    - Organize information
    - Extract key points
    ↓
[Reasoning Bot + Gemini AI]
    - Generate answer
    - Use retrieved context
    - Maintain conversation
    ↓
[Response Formatting Bot]
    - Structure response
    - Add citations
    - Format sources
    ↓
FINAL ANSWER WITH SOURCES
```

### Component Interaction

```
┌────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI                            │
│              (Web Interface for Users)                      │
└────────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────────────────────────┐
        │        FASTAPI BACKEND                │
        │  (14+ REST API Endpoints)             │
        │                                       │
        │  ├─ /ask                             │
        │  ├─ /ingest                          │
        │  ├─ /analytics                       │
        │  └─ /health                          │
        └──────────────────────────────────────┘
                  ↓              ↓
        ┌──────────────┐  ┌──────────────┐
        │ Query Bots   │  │ Embeddings   │
        │ (4 agents)   │  │ Service      │
        └──────────────┘  └──────────────┘
                  ↓              ↓
        ┌──────────────────────────────────────┐
        │  ENDEE VECTOR DATABASE               │
        │  (Primary Vector Storage)            │
        │                                      │
        │  Collections:                        │
        │  ├─ knowledge_base                   │
        │  │  ├─ Dimension: 384                │
        │  │  ├─ Metric: Cosine                │
        │  │  └─ Vectors: Document chunks     │
        │  └─ Metadata: Source, text, score   │
        └──────────────────────────────────────┘
                           ↓
        ┌──────────────────────────────────────┐
        │  GOOGLE GEMINI AI                    │
        │  (LLM for Response Generation)       │
        └──────────────────────────────────────┘
```

---

## How Endee is Used

### 1. Document Ingestion Process

**Step 1: Load Text Files**
```python
documents = load_txt_files("data/")
# Loads: knowledge.txt, guides.txt, etc.
```

**Step 2: Split into Chunks**
```python
chunks = split_text(documents, chunk_size=500, overlap=200)
# Example: 2000-char document → 4-5 chunks with 200-char overlap
```

**Step 3: Generate Embeddings**
```python
embeddings = embedding_model.encode(chunks)
# Converts each chunk to 384-dimensional vector
# Uses: sentence-transformers/all-MiniLM-L6-v2
```

**Step 4: Upsert to Endee**
```python
endee_client.upsert_vectors({
    "id": f"doc_{chunk_id}",
    "vector": embedding,          # 384 floats
    "metadata": {
        "text": chunk_text,       # Original text
        "source": source_file,    # Which file
        "chunk_index": index,     # Position
        "timestamp": datetime.now()
    }
})
```

### 2. Search Process

**User Asks Question:**
```
"What is Endee and how do I use it?"
```

**Convert to Embedding:**
```python
query_embedding = embedding_model.encode(query)
# Same model as documents → comparable embeddings
```

**Search Endee Database:**
```python
results = endee_client.search(
    query_vector=query_embedding,
    limit=5,                      # Get top 5
    with_metadata=True            # Include text & source
)
```

**Endee Returns:**
```python
[
    {
        "id": "doc_0",
        "score": 0.92,            # Cosine similarity
        "metadata": {
            "text": "Endee is a vector database...",
            "source": "endee_guide.txt"
        }
    },
    {
        "id": "doc_1",
        "score": 0.85,
        "metadata": {...}
    }
    # ... more results
]
```

### 3. Response Generation

**Build Context from Retrieved Documents:**
```python
context = "\n\n".join([
    f"Source: {r['metadata']['source']}\n{r['metadata']['text']}"
    for r in results
])
```

**Send to Gemini AI:**
```python
prompt = f"""
Context Information:
{context}

Question: {user_question}

Please answer based on the context above.
Include citations to the source documents.
"""

answer = gemini_model.generate_content(prompt)
```

**Return to User:**
```python
{
    "answer": "Endee is a vector database that...",
    "sources": [
        {"text": "...", "source": "endee_guide.txt", "similarity": 0.92},
        {"text": "...", "source": "guides.txt", "similarity": 0.85}
    ],
    "confidence": 0.88
}
```

---

## Data Processing

### Document Loading
- **Location**: `data/` directory
- **Formats**: Plain text `.txt` files
- **Processing**: Automatic text extraction and cleanup

### Text Chunking Strategy
- **Chunk Size**: 500 characters (configurable)
- **Overlap**: 200 characters (for context continuity)
- **Rationale**: Optimal balance between context and search granularity

### Example Processing
```
documents/knowledge.txt (2000 chars)
    ├─ Chunk 1: [0-500] → Embedding 1 → Endee ID: doc_0
    ├─ Chunk 2: [300-800] → Embedding 2 → Endee ID: doc_1
    ├─ Chunk 3: [600-1100] → Embedding 3 → Endee ID: doc_2
    └─ ... (overlapping chunks)

documents/guides.txt (3000 chars)
    ├─ Chunk 1: [0-500] → Embedding 4 → Endee ID: doc_10
    └─ ... (more chunks)
```

### Embedding Model
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Speed**: ~100 docs/sec on CPU
- **Quality**: High semantic understanding

---

## Installation and Setup

### Prerequisites
```
Python 3.8+
pip or conda
Git
4GB RAM minimum
```

### Step 1: Clone Repository
```bash
git clone https://github.com/abhishek-p-r/endee.git
cd endee
git checkout endee-ai-assistant
```

### Step 2: Create Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Endee Vector Database

#### Option A: Local Installation (Linux/macOS)
```bash
# Clone Endee if separate
git clone https://github.com/endee-io/endee.git
cd endee

# Install and run
chmod +x install.sh run.sh
./install.sh --release --avx2
./run.sh

# Verify: curl http://localhost:8080/health
```

#### Option B: Docker (Recommended)
```bash
# Using provided docker-compose
docker-compose -f docker-compose-app.yml up endee-db

# Or manually:
docker run -p 8080:8080 endee-db
```

### Step 5: Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env with your values:
nano .env
```

**Required variables:**
```env
# Endee vector database
ENDEE_URL=http://localhost:8080
ENDEE_COLLECTION_NAME=knowledge_base

# Google Gemini AI
GEMINI_API_KEY=your_api_key_here

# Optional
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
BACKEND_PORT=8000
STREAMLIT_PORT=8501
```

**Get Gemini API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy key to `.env`

### Step 6: Prepare Documents
```bash
# Create data directory
mkdir -p data

# Add your .txt files
# Example files:
# data/knowledge.txt
# data/guides.txt
# data/faqs.txt
```

---

## How to Run

### Method 1: Automated Start (Easiest - 5 minutes)
```bash
chmod +x start.sh
./start.sh

# Automatically:
# 1. Verifies Endee is running
# 2. Ingests documents from data/
# 3. Creates embeddings
# 4. Stores in Endee database
# 5. Starts backend API (port 8000)
# 6. Starts Streamlit UI (port 8501)

# Opens browser to http://localhost:8501
```

### Method 2: Manual Step-by-Step (10 minutes)

**Terminal 1: Start Endee Server**
```bash
cd endee
./run.sh
# Server starts on http://localhost:8080
# Verify: curl http://localhost:8080/health
```

**Terminal 2: Ingest Documents**
```bash
python scripts/ingest_documents.py \
    --data-dir data/ \
    --endee-url http://localhost:8080 \
    --collection knowledge_base

# Output:
# Loading documents from data/
# Splitting into chunks...
# Generating embeddings...
# Upserting to Endee... (100 vectors)
# ✓ Ingestion complete
```

**Terminal 3: Start Backend API**
```bash
python -m uvicorn backend.main:app \
    --reload \
    --host 0.0.0.0 \
    --port 8000

# API available at: http://localhost:8000
# Swagger UI at: http://localhost:8000/docs
```

**Terminal 4: Start Streamlit UI**
```bash
streamlit run frontend/streamlit_app.py

# Opens automatically at: http://localhost:8501
```

### Method 3: Docker Compose (Production)
```bash
docker-compose -f docker-compose-app.yml up

# Services:
# Endee:  http://localhost:8080
# API:    http://localhost:8000
# UI:     http://localhost:8501

# Stop:
docker-compose -f docker-compose-app.yml down
```

---

## Example Usage

### Using the Web UI (Easiest)

1. **Open Browser**: http://localhost:8501
2. **Type Question**: "How does semantic search work?"
3. **Get Answer**: AI-powered response with sources
4. **View Sources**: See which documents were used

### Using the REST API

**Example 1: Ask a Question**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Endee?",
    "session_id": "user123"
  }'
```

**Response:**
```json
{
  "answer": "Endee is a high-performance open-source vector database built for AI search and retrieval workloads. It's designed for RAG pipelines, semantic search, and recommendation systems.",
  "sources": [
    {
      "text": "Endee is a vector database designed for...",
      "source": "endee_guide.txt",
      "similarity": 0.92
    }
  ],
  "success": true,
  "response_time": 2.3
}
```

**Example 2: Get System Stats**
```bash
curl http://localhost:8000/analytics/stats
```

**Example 3: Optimize a Query**
```bash
curl -X POST "http://localhost:8000/query/optimize" \
  -d "question=what%20is%20endee"
```

### Sample Queries and Results

**Query 1: Definition Question**
```
User: "What is a vector embedding?"

Retrieved: 3 chunks from embeddings_guide.txt

Answer:
"A vector embedding is a numerical representation 
of text that captures semantic meaning. It's a 
fixed-size array of numbers (384 dimensions in 
our case) where similar texts have similar values. 
This enables semantic search by comparing vectors 
using distance metrics like cosine similarity."

Sources:
[1] embeddings_guide.txt - Section: "What are Embeddings?"
[2] embeddings_guide.txt - Section: "Why Use Embeddings?"
```

**Query 2: How-To Question**
```
User: "How do I install Endee?"

Retrieved: 2 chunks from installation_guide.txt

Answer:
"To install Endee locally:
1. Clone: git clone https://github.com/endee-io/endee.git
2. Install: ./install.sh --release --avx2
3. Run: ./run.sh
4. Access: http://localhost:8080

For Docker, use the provided Dockerfile 
for containerized deployment."

Sources:
[1] installation_guide.txt - Section: "Local Installation"
```

---

## Project Structure

```
endee/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
├── start.sh                           # Auto-start script
│
├── backend/                           # FastAPI Application
│   ├── main.py                        # API server & 14 endpoints
│   ├── config.py                      # Configuration
│   ├── logging_config.py              # Logging setup
│   │
│   ├── endee_client.py                # ★ Endee DB client
│   │   ├─ health_check()              # Check server
│   │   ├─ create_collection()         # Create vector store
│   │   ├─ upsert_vectors()            # Store embeddings
│   │   ├─ search()                    # Semantic search
│   │   └─ delete_collection()         # Cleanup
│   │
│   ├── embeddings.py                  # ★ Embedding service
│   │   ├─ generate_embedding()        # Single text → vector
│   │   └─ generate_embeddings_batch() # Multiple texts → vectors
│   │
│   ├── rag_pipeline.py                # ★ RAG orchestration
│   │   └─ process_query()             # Complete pipeline
│   │
│   ├── bots/                          # Multi-agent system
│   │   ├─ query_bot.py                # Optimize queries
│   │   ├─ retrieval_bot.py            # Fetch from Endee
│   │   ├─ reasoning_bot.py            # Generate with Gemini
│   │   └─ formatter_bot.py            # Format response
│   │
│   ├── memory_manager.py              # Conversation history
│   ├── cache_manager.py               # Query caching
│   ├── analytics.py                   # Metrics & stats
│   └── query_optimizer.py             # Query enhancement
│
├── frontend/                          # Streamlit UI
│   ├── streamlit_app.py               # Main interface
│   └── streamlit_enhanced.py          # Enhanced version
│
├── scripts/                           # Utilities
│   ├── ingest_documents.py            # Load & embed docs
│   └── test_api.py                    # API testing
│
├── data/                              # Documents
│   └── (your .txt files here)
│
└── docker-compose-app.yml             # Multi-container setup
```

### Key Components Explained

| File | Purpose | How It Uses Endee |
|------|---------|-------------------|
| `endee_client.py` | Endee communication | HTTP client for all DB operations |
| `embeddings.py` | Text → vectors | Generates embeddings for documents and queries |
| `rag_pipeline.py` | Main orchestration | Coordinates all components |
| `ingest_documents.py` | Document loading | Creates embeddings and stores in Endee |
| `retrieval_bot.py` | Semantic search | Queries Endee and formats results |

---

## API Endpoints

### Query Endpoints
- `POST /ask` - Ask question (returns answer with sources)
- `POST /ask/stream` - Streaming response
- `POST /ask/batch` - Multiple questions at once

### Document Management
- `POST /ingest` - Manual document ingestion
- `POST /ingest/upload` - Upload .txt files
- `GET /documents` - List all documents in Endee
- `DELETE /documents/{id}` - Remove from Endee

### Analytics & Optimization
- `GET /analytics/stats` - System performance metrics
- `GET /analytics/report` - Detailed report
- `POST /query/optimize` - Analyze query before search
- `POST /cache/clear` - Clear result cache

### Health & Info
- `GET /health` - Server status
- `GET /docs` - API documentation (Swagger)

---

## Troubleshooting

### Issue: "Cannot connect to Endee"
```
Error: Connection to Endee failed
Solution: 
  1. Verify Endee is running: curl http://localhost:8080/health
  2. If not, start Endee: cd endee && ./run.sh
  3. Check .env ENDEE_URL is correct
```

### Issue: "Gemini API key not found"
```
Error: GEMINI_API_KEY not found
Solution:
  1. Get API key: https://makersuite.google.com/app/apikey
  2. Add to .env: GEMINI_API_KEY=your_key
  3. Restart application
```

### Issue: "No documents found / No results"
```
Error: Search returns empty results
Solution:
  1. Ingest documents: python scripts/ingest_documents.py
  2. Verify in Endee: curl http://localhost:8080/collections
  3. Check data/ directory has .txt files
```

### Issue: "Slow responses"
```
Solution:
  1. Check cache hit rate: curl http://localhost:8000/analytics/stats
  2. Monitor Endee: curl http://localhost:8080/health
  3. Verify embeddings match dimension: 384
```

---

## Performance Metrics

The system tracks:
- **Query Speed**: Average response time (target: 2-3 seconds)
- **Cache Hit Rate**: % of cached results (target: 50-70%)
- **Success Rate**: % successful queries (target: 95%+)
- **Vector Count**: Total embeddings in Endee
- **System Health**: Endee server status

Access metrics: `http://localhost:8000/analytics/stats`

---

## Architecture Highlights

### Why Endee?
✓ Fast semantic search using cosine similarity
✓ Efficient vector storage (384 dimensions)
✓ Metadata filtering for refined search
✓ HTTP API for easy integration
✓ High-performance similarity matching

### Why This Design?
✓ Multi-agent system (separation of concerns)
✓ Conversation memory (context awareness)
✓ Query optimization (better results)
✓ Caching layer (speed optimization)
✓ Analytics (monitoring & debugging)

---

## Further Reading

- [Endee GitHub](https://github.com/endee-io/endee)
- [Vector Databases Explained](https://www.qdrant.io/articles/vector-database/)
- [RAG Systems](https://huggingface.co/docs/hub/datasets-overview)
- [Semantic Search](https://www.sbert.net/)
- [Gemini API Docs](https://ai.google.dev/)

---

**Built with Endee Vector Database + Gemini AI + Python**
