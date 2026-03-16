# 🚀 Quick Start Guide

Get the Endee AI Knowledge Assistant running in 5 minutes!

## Prerequisites

- Python 3.9+
- [Endee Vector Database](https://github.com/endee-io/endee) (optional - can install later)
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

## Step 1: Clone or Extract Project

```bash
# If you have the project files
cd endee-ai-knowledge-assistant
```

## Step 2: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
nano .env  # or use your editor
```

## Step 5: Start Services

### Option A: Auto Start Script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This will:
- Create necessary directories
- Start the FastAPI backend on port 8000
- Start Streamlit frontend on port 8501
- Ask if you want to ingest sample documents

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/streamlit_app.py
```

**Terminal 3 - Ingest Samples (Optional):**
```bash
python -m scripts.ingest_documents --mode sample
```

### Option C: Docker

```bash
# Start all services with Docker
docker-compose -f docker-compose-app.yml up

# Access:
# - Frontend: http://localhost:8501
# - Backend: http://localhost:8000
```

## Step 6: Access the Application

### Frontend
🌐 **http://localhost:8501**

- Upload documents
- Ask questions
- View chat history
- See source attribution

### Backend API
📚 **http://localhost:8000**

- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## First Run

1. **Open Frontend**: http://localhost:8501
2. **Upload a Document** (optional):
   - Click "📚 Document Upload" in sidebar
   - Upload a PDF, TXT, or Markdown file
   - Click "📤 Upload & Ingest"
3. **Ask Questions**:
   - Type a question in the chat box
   - Example: "What did I upload?" or "Explain vector databases"
4. **View Results**:
   - See the AI answer
   - Click "📊 Response Details" to see sources
   - Check query analysis and key points

## Sample Documents

The system comes with sample documents about:
- Vector databases
- Embeddings and RAG
- FastAPI development
- Multi-agent AI systems

To ingest them:

```bash
# Automatic
python -m scripts.ingest_documents --mode sample

# Or via UI: Click "Upload & Ingest" → It happens in the interface
```

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
python -m uvicorn backend.main:app --port 8001
```

### Frontend won't load
```bash
# Check Streamlit
streamlit run frontend/streamlit_app.py --logger.level=debug

# Update Streamlit
pip install --upgrade streamlit
```

### Gemini API errors
```bash
# Verify API key
echo $GEMINI_API_KEY

# Check API quota at https://makersuite.google.com
```

### Endee connection error
- Endee is optional for initial testing
- To use Endee, download from: https://github.com/endee-io/endee
- Start it separately: `./run.sh`
- Update .env: `ENDEE_URL=http://localhost:8080`

## Common Commands

### Ingest Documents

```bash
# Sample documents
python -m scripts.ingest_documents --mode sample

# Single file
python -m scripts.ingest_documents --mode file --path document.pdf

# Directory
python -m scripts.ingest_documents --mode directory --path ./documents

# Custom source name
python -m scripts.ingest_documents --mode file --path doc.txt --source "My Document"
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a vector database?"}'

# View docs
# Open: http://localhost:8000/docs
```

### Logs

```bash
# View latest logs
tail -f logs/app_*.log

# On Windows
Get-Content logs\app_*.log -Tail 20 -Wait
```

## Next Steps

1. **Read the Full README**
   - `AI_KNOWLEDGE_ASSISTANT_README.md` - Complete documentation

2. **Explore Development**
   - `DEVELOPMENT.md` - Architecture and customization

3. **Upload Your Documents**
   - Use the UI to upload your own documents
   - Support for PDF, TXT, and Markdown

4. **Customize the System**
   - Modify prompts in bot files
   - Change embedding models in config.py
   - Adjust RAG parameters

5. **Deploy to Production**
   - Use Docker containers
   - Configure for your environment
   - Set up monitoring and logging

## Architecture Overview

```
User Question (Web UI)
         ↓
    FastAPI Backend
         ↓
    RAG Pipeline
    ├─ Query Understanding Bot
    ├─ Knowledge Retrieval Bot
    ├─ Reasoning Bot (Gemini AI)
    └─ Formatting Bot
         ↓
   AI-Generated Answer
         ↓
  Web UI Response
```

## Key Features

✅ **Multi-Agent RAG System** - Query understanding, retrieval, reasoning, formatting

✅ **Vector Database Integration** - Endee for semantic search

✅ **LLM Integration** - Google Gemini for answer generation

✅ **Document Management** - Upload and ingest PDF, TXT, MD files

✅ **Conversation Memory** - Context-aware multi-turn conversations

✅ **Source Attribution** - See which documents answered your question

✅ **Modern UI** - Streamlit for easy interaction

✅ **REST API** - FastAPI with automatic documentation

## Example Interactions

### Example 1: Basic Question
```
User: "What is vector embedding?"

System:
1. Optimizes query
2. Searches knowledge base
3. Finds relevant documents
4. Generates answer with Gemini
5. Returns formatted response with sources
```

### Example 2: Document Upload
```
User: Uploads company handbook (PDF)

System:
1. Extracts text from PDF
2. Splits into chunks
3. Generates embeddings
4. Stores in vector database
5. Confirms: "10 chunks stored"
```

### Example 3: Follow-up Question
```
User: "Tell me more about that" (after asking about something)

System:
1. Uses conversation history as context
2. Generates more detailed answer
3. Focuses on previous topic
4. Maintains conversation flow
```

## Performance Tips

- **Batch Ingestion**: Upload multiple files together
- **Chunk Size**: Default 500 is good for most documents
- **Max Results**: Default 5 sources usually sufficient
- **Session Management**: Use unique session IDs for users

## Security Notes

- API Key: Store GEMINI_API_KEY securely
- CORS: Configure for your frontend domain
- Authentication: Add if needed for multi-user
- Rate Limiting: Implement for production use

## Where to Go Next

- **Issues?** Check the troubleshooting section above
- **Want to customize?** See `DEVELOPMENT.md`
- **Need more features?** Check the full `AI_KNOWLEDGE_ASSISTANT_README.md`
- **Questions about Endee?** Visit [endee-io/endee](https://github.com/endee-io/endee)

---

**You're all set!** 🎉

Open http://localhost:8501 and start asking questions!

For detailed documentation, see `AI_KNOWLEDGE_ASSISTANT_README.md`
