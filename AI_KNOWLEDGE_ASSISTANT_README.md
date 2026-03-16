# 🤖 Endee AI Knowledge Assistant - Multi-Agent RAG System

A production-ready AI application showcasing real-world vector database integration with **Endee Vector Database** and **Gemini AI**. This system demonstrates semantic search, RAG pipelines, and intelligent document retrieval.

## 🎯 Project Overview

The Endee AI Knowledge Assistant is a sophisticated multi-agent system that:

- **Accepts user questions** via a modern web interface
- **Understands query intent** using AI-powered query optimization
- **Searches knowledge base** using semantic vector similarity (via Endee)
- **Retrieves relevant context** from stored documents
- **Generates accurate answers** using Google Gemini AI
- **Formats responses** with source attribution and key insights
- **Maintains conversation memory** for context-aware responses

## 🏗️ System Architecture

```
User Question
    ↓
Query Understanding Bot (Intent detection, query optimization)
    ↓
Embedding Generation (SentenceTransformers)
    ↓
Endee Vector Database (Semantic similarity search)
    ↓
Knowledge Retrieval Bot (Fetch relevant chunks)
    ↓
Context Assembly
    ↓
Reasoning & Answer Bot (Gemini AI processing)
    ↓
Response Formatting Bot (Structure and insights)
    ↓
Final Response (Answer + Sources + Key Points)
```

## 🤖 Multi-Agent Bot System

### 1. **Query Understanding Bot**
- Analyzes user questions
- Detects intent (information, comparison, definition, etc.)
- Removes noise from queries
- Optimizes query for semantic search
- Extracts relevant keywords

### 2. **Knowledge Retrieval Bot**
- Generates embeddings for queries
- Searches Endee vector database
- Retrieves top-K relevant documents
- Supports filtered retrieval
- Formats context for LLM

### 3. **Reasoning & Answer Bot**
- Uses Google Gemini AI for generation
- Combines context with user question
- Performs logical reasoning
- Generates comprehensive answers
- Incorporates conversation history

### 4. **Response Formatting Bot**
- Improves text readability
- Extracts key points
- Highlights important insights
- Structures final output
- Adds source attribution

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **LLM**: Google Gemini API
- **Vector Database**: Endee (localhost:8080)
- **Dependencies**: Pydantic, httpx, requests

### Frontend
- **UI Framework**: Streamlit (reactive web UI)
- **Language**: Python
- **Communication**: REST API calls

### Vector Database
- **Endee**: Open-source vector database
- **Features**: Fast similarity search, filtered retrieval, scalable storage

## 📦 Project Structure

```
endee-ai-knowledge-assistant/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── embeddings.py           # Embedding service (SentenceTransformers)
│   ├── endee_client.py         # Endee vector DB HTTP client
│   ├── gemini_client.py        # Google Gemini AI client
│   ├── memory_manager.py       # Conversation history management
│   ├── rag_pipeline.py         # Complete RAG orchestration
│   ├── logging_config.py       # Logging configuration
│   └── bots/
│       ├── __init__.py
│       ├── query_bot.py        # Query understanding & optimization
│       ├── retrieval_bot.py    # Knowledge retrieval from Endee
│       ├── reasoning_bot.py    # Answer generation with Gemini
│       └── formatter_bot.py    # Response formatting & insights
├── frontend/
│   └── streamlit_app.py        # Streamlit user interface
├── scripts/
│   └── ingest_documents.py     # Batch document ingestion script
├── data/
│   └── knowledge_base/         # Storage for uploaded documents
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # This file
```

## ⚡ Key Features

### ✨ Smart Query Processing
- Intelligent query understanding
- Intent detection
- Automatic query optimization
- Keyword extraction

### 🔍 Semantic Search
- Vector-based similarity search
- Filtered retrieval options
- Relevance scoring
- Top-K retrieval

### 💬 Conversational AI
- Multi-turn conversations
- Conversation memory/history
- Context-aware responses
- Session management

### 📚 Document Management
- Support for PDF, TXT, MD files
- Automatic chunking
- Batch ingestion
- Metadata tracking

### 📊 Rich Response Format
- Clear, structured answers
- Key points extraction
- Source attribution
- Confidence scoring

### 🔐 Production Ready
- Comprehensive error handling
- Logging system
- Health checks
- CORS support
- Async operations

## 🚀 Getting Started

### Prerequisites

1. **Python 3.9+**
2. **Endee Vector Database** running on localhost:8080
3. **Google Gemini API Key** (get from https://makersuite.google.com/app/apikey)

### 1. Install Endee Vector Database

```bash
# Clone and install Endee
git clone https://github.com/endee-io/endee.git
cd endee

chmod +x install.sh run.sh
./install.sh --release --avx2
./run.sh

# Server will start on http://localhost:8080
```

### 2. Setup Project Environment

```bash
# Clone or extract the project
cd endee-ai-knowledge-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Required variables:
# GEMINI_API_KEY=your_api_key_here
# ENDEE_URL=http://localhost:8080
```

### 4. Run the Backend

```bash
# Start FastAPI server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Server will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 5. Run the Frontend

```bash
# In a new terminal
streamlit run frontend/streamlit_app.py

# Frontend will open at http://localhost:8501
```

### 6. Ingest Sample Documents (Optional)

```bash
# In another terminal
python -m scripts.ingest_documents --mode sample

# Or ingest your own file:
python -m scripts.ingest_documents --mode file --path /path/to/document.pdf
```

## 📚 API Endpoints

### Health Check
```bash
GET /health
# Returns: {"status": "healthy", "service": "...", "endee_connected": true}
```

### Ask Question
```bash
POST /ask
Content-Type: application/json

{
  "question": "What is a vector database?",
  "session_id": "user_123",
  "use_conversation_history": true
}

# Returns: {"success": true, "answer": "...", "sources": [...], ...}
```

### Ingest Documents
```bash
POST /ingest
Content-Type: application/json

{
  "documents": [
    {"text": "Document content...", "source": "Doc 1"}
  ],
  "chunk_size": 500,
  "chunk_overlap": 50
}

# Returns: {"success": true, "documents_ingested": 1, "vectors_stored": 5, ...}
```

### Upload & Ingest File
```bash
POST /ingest/upload
Content-Type: multipart/form-data

file: <your_file>
source: Optional source name

# Returns: {"success": true, "vectors_stored": 10, ...}
```

### Get Chat History
```bash
GET /chat/history/{session_id}
# Returns: {"session_id": "...", "messages": [...]}
```

### Clear Chat History
```bash
DELETE /chat/history/{session_id}
# Returns: {"message": "Chat history cleared..."}
```

## 🎨 Frontend Features

### Chat Interface
- Real-time question answering
- Message history display
- Responsive design

### Document Upload
- Drag-and-drop file upload
- Support for PDF, TXT, MD formats
- Progress indication

### Response Details
- View retrieved sources
- See query analysis
- Extract key points
- Check relevance scores

### Session Management
- Unique session identifiers
- Conversation memory
- History management

## 🧪 Example Usage

### Example 1: Asking About Vector Databases
```
User: "What is a vector database and how does it work?"

System:
1. Optimizes query for search
2. Searches knowledge base
3. Retrieves relevant documents
4. Generates answer with Gemini
5. Returns formatted response with sources
```

### Example 2: Batch Document Ingestion
```bash
python -m scripts.ingest_documents --mode directory --path ./documents
```

### Example 3: API Integration
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={
        "question": "How do embeddings work?",
        "session_id": "user_1"
    }
)

answer = response.json()
print(answer['answer'])
print(answer['sources'])
```

## 🔧 Configuration

Edit `.env` file to customize:

- **GEMINI_API_KEY**: Your Google Gemini API key
- **ENDEE_URL**: Endee server URL
- **SERVER_HOST/PORT**: FastAPI server configuration
- **CHUNK_SIZE**: Document chunk size (default: 500)
- **MAX_RETRIEVED_DOCUMENTS**: Number of documents to retrieve (default: 5)
- **EMBEDDING_MODEL**: Model for generating embeddings

## 📊 Logging

Logs are saved in the `logs/` directory with:
- Daily log files
- Automatic rotation
- Detailed error tracking
- Performance metrics

## 🐳 Docker Deployment (Optional)

```dockerfile
# Build
docker build -t endee-assistant .
docker-compose up -d

# The services will be available at:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:8501
# - Endee: http://localhost:8080
```

## 🚨 Troubleshooting

### Backend connection error
- Ensure FastAPI is running: `python -m uvicorn backend.main:app --reload`
- Check if port 8000 is available

### Endee connection error
- Ensure Endee server is running on localhost:8080
- Check: `curl http://localhost:8080/health`

### Gemini API error
- Verify GEMINI_API_KEY is set correctly
- Check API quota and permissions

### Embedding generation error
- Ensure SentenceTransformers model is downloaded
- Check disk space for model cache

## 📈 Performance Tips

1. **Batch Processing**: Use batch ingestion for multiple documents
2. **Caching**: Frontend caches health checks
3. **Async Operations**: All I/O operations are async
4. **Chunking**: Optimize chunk size for your documents
5. **Indexing**: Endee automatically optimizes for search

## 🔐 Security Considerations

1. **API Keys**: Store Gemini API key securely
2. **CORS**: Configure CORS for frontend domain
3. **Rate Limiting**: Implement rate limiting for production
4. **Authentication**: Add auth for multi-user deployments
5. **Validation**: All inputs are validated with Pydantic

## 📝 Example Documents

Sample documents are provided covering:
- Endee Vector Database guide
- Vector embeddings fundamentals
- RAG system architecture
- Multi-agent AI systems
- FastAPI best practices

## 🎓 Learning Resources

- [Endee GitHub](https://github.com/endee-io/endee)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SentenceTransformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)

## 📄 License

This project is provided as an educational demonstration of vector database and RAG system integration.

## 🤝 Contributing

Feel free to extend this project with:
- Additional embedding models
- Different LLM providers
- Enhanced UI components
- Performance optimizations
- Additional bot types

## 📞 Support

For issues with:
- **Endee**: Check [Endee Documentation](https://github.com/endee-io/endee)
- **Gemini API**: Check [Google AI Documentation](https://ai.google.dev/)
- **FastAPI**: Check [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Built with ❤️ to showcase the power of vector databases and AI-powered retrieval systems.**

Last Updated: March 2026
