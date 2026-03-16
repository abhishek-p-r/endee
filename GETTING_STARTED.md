# Getting Started with Endee AI Knowledge Assistant

Welcome! This guide walks you through everything you need to get the Endee AI Knowledge Assistant up and running.

## 📖 Documentation Map

Choose your path based on what you need:

### 🏃 Quick Start (5 minutes)
- **File**: `QUICKSTART.md`
- **For**: Those who want to run it immediately
- **Contains**: Basic setup, prerequisites, and first run

### 📚 Full Documentation (Comprehensive)
- **File**: `AI_KNOWLEDGE_ASSISTANT_README.md`
- **For**: Understanding the complete system
- **Contains**: Architecture, features, API docs, examples

### 👨‍💻 Development Guide
- **File**: `DEVELOPMENT.md`
- **For**: Customization, extending features
- **Contains**: Code structure, adding features, debugging

### 🗺️ Project Structure
- **File**: `PROJECT_STRUCTURE.md`
- **For**: Finding files and understanding organization
- **Contains**: File descriptions, dependencies, navigation

### 🔧 This File
- **Current**: `GETTING_STARTED.md`
- **For**: Choosing the right path
- **Contains**: Navigation and setup overview

## 🚀 Choose Your Setup Path

### Path 1: Super Quick (No Endee Database Required)

**Time**: 3-5 minutes | **Complexity**: Easy

You can test the system without installing Endee initially.

```bash
# 1. Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add GEMINI_API_KEY=your_key

# 4. Start services
# Terminal 1: Backend
python -m uvicorn backend.main:app --reload

# Terminal 2: Frontend
streamlit run frontend/streamlit_app.py
```

Visit: http://localhost:8501

**Note**: Vector search will show warnings without Endee, but you can still test the system.

### Path 2: Complete Installation (With Endee)

**Time**: 10-15 minutes | **Complexity**: Medium

Full production-ready setup with vector database.

```bash
# 1. Install Endee Vector Database
git clone https://github.com/endee-io/endee.git
cd endee
chmod +x install.sh run.sh
./install.sh --release --avx2
./run.sh
# Endee will start on localhost:8080

# 2. Setup AI Assistant (in new terminal)
cd endee-ai-knowledge-assistant
python -m venv venv
source venv/bin/activate

# 3. Install and configure
pip install -r requirements.txt
cp .env.example .env
# Edit .env with GEMINI_API_KEY

# 4. Use convenience script
chmod +x start.sh
./start.sh
```

This will start everything and offer to ingest sample documents.

### Path 3: Docker Everything

**Time**: 5 minutes | **Complexity**: Easy (if Docker installed)

```bash
# Make sure Docker and Docker Compose are installed

docker-compose -f docker-compose-app.yml up

# Services available at:
# - Frontend: http://localhost:8501
# - Backend: http://localhost:8000
# - Endee: http://localhost:8080
```

## 🎯 What You'll Have After Setup

### Web Interface (Streamlit)
- **URL**: http://localhost:8501
- **Features**: 
  - Chat interface for asking questions
  - Document upload (PDF, TXT, MD)
  - View conversation history
  - See source attribution

### API Backend (FastAPI)
- **URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Features**:
  - REST API endpoints
  - Auto-generated documentation
  - Health checks

### Vector Database (Endee)
- **URL**: http://localhost:8080
- **Features**:
  - Fast similarity search
  - Vector storage
  - Filtered retrieval

## 🔑 Required: Gemini API Key

Get your free API key:

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Click "Create API Key in new project"
4. Copy the key
5. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## 🧪 Quick Test

After setup, test with these commands:

### Test Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Endee AI Knowledge Assistant",
  "endee_connected": true
}
```

### Test Question Answering
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a vector database?"}'
```

### Test Document Ingestion
```bash
python -m scripts.ingest_documents --mode sample
```

## 📊 System Architecture

```
┌─────────────────────────────────────┐
│   Streamlit Web Interface :8501    │
│  (Upload docs, Ask questions)      │
└────────────────┬────────────────────┘
                 │ HTTP
                 ▼
┌─────────────────────────────────────┐
│  FastAPI Backend :8000              │
│  ├─ RAG Pipeline                   │
│  ├─ Query Understanding Bot        │
│  ├─ Knowledge Retrieval Bot        │
│  ├─ Reasoning Bot (Gemini)         │
│  └─ Response Formatting Bot        │
└────────┬──────────────┬────────────┘
         │              │
         ▼              ▼
    Endee DB       Gemini AI
    :8080         (Google API)
```

## 🆘 Common Issues & Solutions

### Issue: "Backend Connection Refused"
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running, start it:
python -m uvicorn backend.main:app --reload
```

### Issue: "GEMINI_API_KEY not found"
```bash
# Verify .env file exists
cat .env

# Check the key is set
echo $GEMINI_API_KEY

# If empty, edit .env
nano .env  # Add GEMINI_API_KEY=your_key
```

### Issue: "Endee connection error"
- Endee is optional for initial testing
- If you want vector search:
  ```bash
  # Start Endee separately
  cd endee && ./run.sh
  
  # Update .env
  ENDEE_URL=http://localhost:8080
  ```

### Issue: "Port already in use"
```bash
# Use different ports
python -m uvicorn backend.main:app --port 8001
streamlit run frontend/streamlit_app.py --server.port 8502
```

## 📚 Next Steps

### 1. Familiarize Yourself
- Visit http://localhost:8501
- Ask test questions
- Upload a document
- Check out the response details

### 2. Try Sample Documents
```bash
python -m scripts.ingest_documents --mode sample
```

### 3. Upload Your Own Documents
- Click "📚 Document Upload" in Streamlit
- Upload PDF, TXT, or Markdown files
- Ask questions about your documents

### 4. Explore the API
- Visit http://localhost:8000/docs
- Try endpoints in the interactive UI
- Read full API documentation

### 5. Customize the System
- Read `DEVELOPMENT.md` for details
- Modify bots in `backend/bots/`
- Change prompts for different behaviors
- Adjust RAG parameters in `config.py`

## 🎓 Learning Resources

### Understand the Technology
- **Vector Databases**: https://github.com/endee-io/endee
- **RAG Systems**: https://en.wikipedia.org/wiki/Retrieval-augmented_generation
- **LLMs**: https://ai.google.dev/
- **Embeddings**: https://www.sbert.net/

### Framework Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://docs.streamlit.io/
- **SentenceTransformers**: https://www.sbert.net/

## 🔍 File Reference

| Document | When to Read | Main Topics |
|----------|--------------|------------|
| QUICKSTART.md | Getting running fast | Setup, prerequisites, first run |
| AI_KNOWLEDGE_ASSISTANT_README.md | Understanding system | Features, architecture, API docs |
| DEVELOPMENT.md | Modifying code | Code structure, adding features |
| PROJECT_STRUCTURE.md | Finding files | File descriptions, navigation |
| GETTING_STARTED.md | This file | Setup paths, navigation |

## 🚀 Ready to Start?

### Fastest Way
```bash
chmod +x start.sh
./start.sh
```
Opens everything and offers to ingest sample documents.

### Standard Way
Follow Path 2 or 3 above.

### Details
Read `QUICKSTART.md` for step-by-step instructions.

## ❓ Questions?

### About the AI Assistant
- Read `AI_KNOWLEDGE_ASSISTANT_README.md`
- Check `DEVELOPMENT.md` for customization

### About Endee
- Visit: https://github.com/endee-io/endee
- Check: https://docs.endee.ai

### About Gemini API
- Visit: https://ai.google.dev/
- Check: https://makersuite.google.com

## 📋 Checklist

Before you start:
- [ ] Python 3.9+ installed
- [ ] Gemini API key obtained
- [ ] Port 8000, 8501, 8080 available
- [ ] 2-3 GB disk space available
- [ ] Internet connection (for model downloads)

After setup:
- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:8501
- [ ] Health check returns 200
- [ ] Can ask questions
- [ ] Can upload documents

## 🎉 You're Ready!

Start with one of the setup paths above and follow the instructions. Most people get running in under 10 minutes!

For detailed information, see the other documentation files.

---

**Questions? Issues? See the troubleshooting section above or read the full documentation files.**

Last Updated: March 2026
