# Endee AI Knowledge Assistant

A sophisticated multi-agent RAG (Retrieval-Augmented Generation) system powered by Endee vector database and Google Gemini AI.

## Quick Links

- **New Users?** Start here: [HOW_TO_RUN.md](./HOW_TO_RUN.md) - Complete step-by-step guide
- **5-minute setup?** [QUICKSTART.md](./QUICKSTART.md) - Fast setup for experienced users
- **Want details?** [AI_KNOWLEDGE_ASSISTANT_README.md](./AI_KNOWLEDGE_ASSISTANT_README.md) - Full documentation

---

## What is Endee AI Knowledge Assistant?

An intelligent system that understands your questions and finds answers from your documents using:

1. **Vector Search** - Semantic understanding of your documents
2. **Multi-Agent AI** - 4 specialized AI agents working together:
   - Query Understanding Bot
   - Knowledge Retrieval Bot
   - Reasoning Bot (Gemini AI)
   - Response Formatting Bot
3. **Google Gemini** - State-of-the-art language model for answer generation

---

## Installation & Running

### The Fastest Way (5 minutes)

```bash
# 1. Get to the project
cd endee-ai-knowledge-assistant

# 2. Run the startup script
chmod +x start.sh
./start.sh

# 3. Enter your Gemini API key when prompted
# Get free key: https://makersuite.google.com/app/apikey

# 4. Open in browser
# Frontend: http://localhost:8501
# Backend: http://localhost:8000/docs
```

### For Detailed Instructions

See [HOW_TO_RUN.md](./HOW_TO_RUN.md) for:
- System requirements
- Step-by-step setup
- Running with Docker
- Troubleshooting
- Advanced configuration

---

## Architecture

```
                    User Question
                         ↓
                  Web UI (Streamlit)
                         ↓
                  FastAPI Backend
                         ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
   Query Bot    Retrieval Bot    Reasoning Bot
   (Optimize)    (Search)         (Gemini AI)
        ↓                 ↓                 ↓
        └─────────────────┼─────────────────┘
                         ↓
                  Formatting Bot
                         ↓
                  Final Response
                         ↓
                  Web UI Display
```

### Components

**Frontend:**
- Streamlit web application
- Real-time chat interface
- Document upload capability
- Session management

**Backend:**
- FastAPI REST API
- RAG Pipeline (Query → Retrieve → Reason → Format)
- Vector embeddings with SentenceTransformers
- Conversation memory management

**AI Models:**
- SentenceTransformers for embeddings
- Google Gemini for answer generation
- Endee vector database for storage & retrieval

---

## Key Features

✅ **Multi-Agent System** - 4 specialized AI bots working together

✅ **Document Management** - Upload PDF, TXT, Markdown files

✅ **Semantic Search** - Find information by meaning, not just keywords

✅ **Conversation Memory** - Context-aware multi-turn conversations

✅ **Source Attribution** - See which documents answered your question

✅ **REST API** - Full API for programmatic access

✅ **Modern UI** - Clean Streamlit interface

✅ **Docker Ready** - Container deployment included

✅ **Scalable** - Handles thousands of documents

---

## Project Structure

```
endee-ai-knowledge-assistant/
├── backend/                          # Python backend
│   ├── bots/                        # AI agents
│   │   ├── query_bot.py            # Query optimization
│   │   ├── retrieval_bot.py        # Knowledge retrieval
│   │   ├── reasoning_bot.py        # Answer generation
│   │   └── formatter_bot.py        # Response formatting
│   ├── rag_pipeline.py             # RAG orchestration
│   ├── embeddings.py               # Vector embeddings
│   ├── gemini_client.py            # Gemini API integration
│   ├── endee_client.py             # Endee vector DB client
│   ├── memory_manager.py           # Conversation memory
│   ├── main.py                     # FastAPI server
│   ├── config.py                   # Configuration
│   └── logging_config.py           # Logging setup
│
├── frontend/
│   └── streamlit_app.py            # Web UI
│
├── scripts/
│   ├── ingest_documents.py         # Document processing
│   └── test_api.py                 # API testing
│
├── docs/                           # Documentation
├── logs/                           # Application logs
├── data/                           # Embeddings & vectors
│
├── HOW_TO_RUN.md                   # THIS FILE - Setup guide
├── QUICKSTART.md                   # 5-minute setup
├── AI_KNOWLEDGE_ASSISTANT_README.md  # Full documentation
├── DEVELOPMENT.md                  # Architecture & customization
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── Dockerfile                      # Container definition
├── docker-compose-app.yml          # Multi-service deployment
└── start.sh                        # Startup script
```

---

## Running the Application

### Option 1: Automated Script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual - Three Terminals

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
source venv/bin/activate
streamlit run frontend/streamlit_app.py
```

**Terminal 3 - Documents (Optional):**
```bash
source venv/bin/activate
python -m scripts.ingest_documents --mode sample
```

### Option 3: Docker

```bash
docker-compose -f docker-compose-app.yml up
```

---

## Accessing the Application

After starting:

- **Frontend UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Example Usage

### Via Web UI

1. Open http://localhost:8501
2. Upload a document (PDF, TXT, or Markdown)
3. Ask a question: "What is this document about?"
4. View the AI response with source attribution

### Via API

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is vector embedding?",
    "session_id": "user-123",
    "top_k": 5
  }'
```

Response:
```json
{
  "answer": "Vector embedding is...",
  "sources": [
    {
      "source": "document.pdf",
      "content": "..."
    }
  ],
  "query_analysis": {
    "original": "What is vector embedding?",
    "optimized": "vector embedding concept definition"
  }
}
```

---

## Configuration

### Environment Variables

Create `.env` file:

```env
# REQUIRED: Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# OPTIONAL: Vector database URL
ENDEE_URL=http://localhost:8080

# OPTIONAL: Embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# OPTIONAL: Logging level
LOG_LEVEL=INFO
```

Get your free Gemini API key: https://makersuite.google.com/app/apikey

### Customize Settings

Edit `backend/config.py`:
- Chunk size for documents
- Number of sources to retrieve
- Embedding model
- Logging configuration

---

## API Endpoints

### Health & Info

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if system is running |
| `/info` | GET | Get system information |

### Questions & Answers

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ask` | POST | Ask a question |
| `/analyze-query` | POST | Analyze and optimize a query |
| `/chat/{session_id}` | GET | Get chat history |

### Document Management

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/upload` | POST | Upload a document |
| `/documents` | GET | List ingested documents |
| `/documents/{id}` | DELETE | Remove a document |

Full API documentation at: http://localhost:8000/docs

---

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
python -m uvicorn backend.main:app --port 8001
```

### Dependencies Not Found

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### API Key Error

1. Get free key: https://makersuite.google.com/app/apikey
2. Add to `.env`: `GEMINI_API_KEY=your_key`
3. Restart the application

### More Issues?

See [HOW_TO_RUN.md](./HOW_TO_RUN.md#troubleshooting) for detailed troubleshooting guide.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [HOW_TO_RUN.md](./HOW_TO_RUN.md) | Complete setup & troubleshooting |
| [QUICKSTART.md](./QUICKSTART.md) | 5-minute rapid setup |
| [AI_KNOWLEDGE_ASSISTANT_README.md](./AI_KNOWLEDGE_ASSISTANT_README.md) | Full feature documentation |
| [DEVELOPMENT.md](./DEVELOPMENT.md) | Architecture & customization |
| [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) | File organization |

---

## Getting Started

1. **First time?** Start with [HOW_TO_RUN.md](./HOW_TO_RUN.md)
2. **In a hurry?** Check [QUICKSTART.md](./QUICKSTART.md)
3. **Need details?** Read [AI_KNOWLEDGE_ASSISTANT_README.md](./AI_KNOWLEDGE_ASSISTANT_README.md)
4. **Want to customize?** See [DEVELOPMENT.md](./DEVELOPMENT.md)

---

## System Requirements

- Python 3.9+
- 4 GB RAM (8 GB recommended)
- 2 GB disk space
- Google Gemini API key (free)
- Internet connection for LLM API

---

## Performance

- **Small documents** (1-50 MB): < 2 seconds
- **Medium documents** (50-500 MB): 2-10 seconds
- **Large documents** (500+ MB): Batch processing recommended
- **Concurrent requests**: Up to 10 simultaneously

---

## Technology Stack

**Backend:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SentenceTransformers (embeddings)
- google-generativeai (Gemini API)

**Frontend:**
- Streamlit (web UI)
- Python (application logic)

**Database:**
- Endee (vector database, optional)
- In-memory fallback for testing

**Deployment:**
- Docker (containerization)
- Python venv (local development)

---

## Next Steps

### Immediate
1. Run `./start.sh` or follow [HOW_TO_RUN.md](./HOW_TO_RUN.md)
2. Access http://localhost:8501
3. Upload a document
4. Ask a question

### Short Term
- Customize prompts in `backend/bots/`
- Adjust RAG parameters in `backend/config.py`
- Fine-tune embedding model selection

### Long Term
- Set up Endee vector database
- Deploy to production with Docker
- Integrate with your applications
- Set up monitoring and logging

---

## Support & Community

- **Issues?** See [HOW_TO_RUN.md#troubleshooting](./HOW_TO_RUN.md#troubleshooting)
- **Questions?** Check the documentation files
- **Endee help?** Visit [endee.io](https://endee.io/)
- **Gemini help?** Visit [ai.google.dev](https://ai.google.dev)

---

## License

This Endee AI Knowledge Assistant is part of the Endee project.
See [LICENSE](./LICENSE) for details.

---

**Ready to get started?** Jump to [HOW_TO_RUN.md](./HOW_TO_RUN.md) now! 🚀
