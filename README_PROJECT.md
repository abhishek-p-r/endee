# Endee AI Knowledge Assistant 🤖

**A production-ready Multi-Agent RAG System powered by Endee Vector Database and Google Gemini AI**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What This Project Does

Transform how you interact with your knowledge:

1. **Upload Documents** → PDF, TXT, or Markdown files
2. **Store Intelligently** → Automatic chunking and vector embeddings
3. **Search Semantically** → Find relevant information using AI-powered search
4. **Ask Questions** → Natural language queries about your documents
5. **Get Smart Answers** → AI-generated responses with source attribution

## ✨ Key Features

- 🤖 **Multi-Agent RAG System** - 4 specialized AI bots working together
- 📚 **Vector Database Integration** - Endee for high-performance similarity search
- 💬 **Conversation Memory** - Context-aware multi-turn conversations
- 📄 **Smart Document Processing** - Automatic chunking, embedding, storage
- 🎯 **Query Optimization** - Intent detection and query refinement
- 📊 **Source Attribution** - See exactly which documents answered your question
- 🌐 **Modern Web UI** - Streamlit interface with real-time interactions
- 📡 **REST API** - FastAPI with auto-generated documentation
- 🔍 **Flexible Search** - Semantic similarity + metadata filtering
- 🚀 **Production Ready** - Professional error handling, logging, monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Web Interface (Streamlit)         │
│   Upload docs • Ask questions       │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│   FastAPI Backend (:8000)           │
├─────────────────────────────────────┤
│   RAG Pipeline Orchestration        │
├─────────────────────────────────────┤
│   4 AI Bots                         │
│   • Query Understanding Bot        │
│   • Knowledge Retrieval Bot        │
│   • Reasoning & Answer Bot         │
│   • Response Formatting Bot        │
├─────────────────────────────────────┤
│   Supporting Services              │
│   • Embeddings (SentenceTransformers)
│   • Memory Management              │
│   • Logging & Error Handling       │
└─────────┬──────────────────┬────────┘
          │                  │
    ┌─────▼─────┐      ┌─────▼──────┐
    │ Endee DB  │      │ Gemini API │
    │ :8080     │      │            │
    │ Vector    │      │ Answer     │
    │ Storage   │      │ Generation │
    └───────────┘      └────────────┘
```

## 🚀 Quick Start

### 5-Minute Setup

```bash
# 1. Clone/Extract and setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# 3. Run
chmod +x start.sh
./start.sh
```

**That's it!** Open http://localhost:8501

### With Docker

```bash
docker-compose -f docker-compose-app.yml up
```

Full setup details in **[QUICKSTART.md](QUICKSTART.md)**

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get running in 5 minutes |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Choose your setup path |
| **[AI_KNOWLEDGE_ASSISTANT_README.md](AI_KNOWLEDGE_ASSISTANT_README.md)** | Complete documentation |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Customize and extend |
| **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** | File organization |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | What was built |

## 🎯 How It Works

### The RAG Pipeline

```
User Question
    ↓
Query Understanding Bot
  ├─ Detect intent
  ├─ Optimize query
  └─ Extract keywords
    ↓
Embedding Generation
  └─ Convert to vector
    ↓
Knowledge Retrieval Bot
  ├─ Search Endee database
  ├─ Find similar documents
  └─ Rank by relevance
    ↓
Context Assembly
  └─ Format retrieved knowledge
    ↓
Reasoning & Answer Bot
  ├─ Combine context + question
  ├─ Use Gemini AI
  └─ Generate comprehensive answer
    ↓
Response Formatting Bot
  ├─ Improve readability
  ├─ Extract key points
  ├─ Add source attribution
  └─ Structure output
    ↓
Final Response to User
```

## 🧠 The 4 AI Bots

### 1. Query Understanding Bot 🔍
- Analyzes user intent
- Removes noise from queries
- Optimizes for semantic search
- Extracts keywords

### 2. Knowledge Retrieval Bot 📚
- Generates embeddings
- Searches vector database
- Retrieves relevant chunks
- Ranks by relevance

### 3. Reasoning & Answer Bot 🤖
- Combines context with question
- Uses Gemini AI for generation
- Performs logical reasoning
- Generates accurate answers

### 4. Response Formatting Bot ✨
- Improves text readability
- Extracts key insights
- Highlights important points
- Adds source attribution

## 📊 API Endpoints

```bash
# Health check
GET /health

# Ask a question
POST /ask
{
  "question": "What is RAG?",
  "session_id": "user_123",
  "use_conversation_history": true
}

# Ingest documents
POST /ingest
{
  "documents": [
    {"text": "...", "source": "..."}
  ]
}

# Upload file
POST /ingest/upload
File: <document.pdf>

# Get chat history
GET /chat/history/{session_id}

# Clear history
DELETE /chat/history/{session_id}
```

Full API docs at: http://localhost:8000/docs

## 💻 Use Cases

### 📚 Knowledge Base Assistant
- Company handbook Q&A
- Product documentation search
- Policy lookup

### 🔬 Research Assistant
- Paper summarization
- Citation finding
- Concept explanation

### 💼 Business Intelligence
- Document analysis
- Report summarization
- Insight extraction

### 🎓 Learning Assistant
- Concept explanation
- Study material review
- Question answering

### 📖 Content Discovery
- Similar content finding
- Topic exploration
- Knowledge graph building

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Web Framework**: FastAPI (async, modern)
- **UI Framework**: Streamlit (reactive)
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **LLM**: Google Gemini API
- **Vector Database**: Endee (high-performance)
- **Server**: Uvicorn (ASGI)
- **Data Validation**: Pydantic
- **HTTP Client**: httpx (async)
- **Deployment**: Docker, Docker Compose

## 📋 Requirements

- Python 3.9 or higher
- 2-3 GB disk space
- Google Gemini API key (free at https://makersuite.google.com/app/apikey)
- Internet connection (for model downloads)
- Endee Vector Database (optional - will warn but work without)

## 🔧 Configuration

Create `.env` file:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional with defaults
ENDEE_URL=http://localhost:8080
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False

# RAG Settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50
MAX_RETRIEVED_DOCUMENTS=5
SIMILARITY_THRESHOLD=0.3
```

## 🧪 Testing

### Test the API

```bash
python -m scripts.test_api --url http://localhost:8000

# Run specific test
python -m scripts.test_api --test health
python -m scripts.test_api --test ask --question "Your question"
```

### Ingest Sample Documents

```bash
python -m scripts.ingest_documents --mode sample
```

### Manual Testing

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a vector database?"}'
```

## 📚 Learn More

### About This Project
- [Complete Documentation](AI_KNOWLEDGE_ASSISTANT_README.md)
- [Architecture & Customization](DEVELOPMENT.md)
- [Project Structure](PROJECT_STRUCTURE.md)

### External Resources
- [Endee Vector Database](https://github.com/endee-io/endee)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [RAG Explanation](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

## 🎯 Getting Help

### Common Issues

**Backend won't connect?**
```bash
curl http://localhost:8000/health
```

**Gemini API error?**
- Get key: https://makersuite.google.com/app/apikey
- Add to .env: `GEMINI_API_KEY=your_key`

**Endee not found?**
- Optional dependency
- Start it: `cd endee && ./run.sh`
- Update .env: `ENDEE_URL=http://localhost:8080`

See [QUICKSTART.md](QUICKSTART.md) for more troubleshooting.

## 🚀 Deployment

### Development
```bash
./start.sh
```

### Production
```bash
docker-compose -f docker-compose-app.yml up -d
```

### Manual Setup
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## 🔐 Security Notes

- Store API keys securely
- Configure CORS for your domain
- Use HTTPS in production
- Enable authentication for multi-user
- Implement rate limiting
- Monitor logs regularly

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Python Files | 16 |
| Lines of Code | 2,500+ |
| API Endpoints | 6+ |
| AI Bots | 4 |
| Documentation Pages | 6 |
| Supported File Types | 3 (PDF, TXT, MD) |
| Dependencies | 15 |

## 🎓 Educational Value

Learn about:
- ✅ RAG (Retrieval Augmented Generation) systems
- ✅ Vector databases and embeddings
- ✅ Multi-agent AI architecture
- ✅ Modern Python web development
- ✅ Async/await patterns
- ✅ Type-safe code with Pydantic
- ✅ Professional software engineering

## 🤝 Contributing

Ideas for extending:
- Additional embedding models (OpenAI, Cohere)
- Different LLM providers (Claude, GPT, Llama)
- Custom bot types
- Advanced filtering options
- Performance optimizations
- UI enhancements
- Database integrations

## 📜 License

This project is provided for educational and commercial use.

## 🙌 Acknowledgments

Built with:
- [Endee Vector Database](https://github.com/endee-io/endee)
- [Google Gemini API](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [SentenceTransformers](https://www.sbert.net/)

## 🚀 Ready to Start?

```bash
# Option 1: Fastest
chmod +x start.sh && ./start.sh

# Option 2: With Docker
docker-compose -f docker-compose-app.yml up

# Option 3: Step by step
# Read QUICKSTART.md
```

Open **http://localhost:8501** and start asking questions!

---

## 📞 Quick Links

- 🏃 **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- 🗺️ **Navigation**: [GETTING_STARTED.md](GETTING_STARTED.md)
- 📚 **Full Docs**: [AI_KNOWLEDGE_ASSISTANT_README.md](AI_KNOWLEDGE_ASSISTANT_README.md)
- 👨‍💻 **Development**: [DEVELOPMENT.md](DEVELOPMENT.md)
- 🗂️ **Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- ✅ **Implementation**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

---

**Status**: ✅ Complete and Production-Ready

**Last Updated**: March 2026

Built with ❤️ to showcase the power of vector databases and AI-powered retrieval systems.
