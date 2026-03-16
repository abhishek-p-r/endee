# 🚀 Endee AI Knowledge Assistant - Startup Guide

Complete step-by-step guide to run the production-ready system.

## ⚡ Quick Start (5 minutes)

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/abhishek-p-r/endee.git
cd endee

# 2. Create environment file
cp .env.example .env

# 3. Add your OpenAI API key
# Edit .env and set: OPENAI_API_KEY=sk-your-key-here

# 4. Add sample documents (optional)
mkdir -p data
# Place your .txt, .pdf, or .md files in data/

# 5. Start all services
docker-compose -f docker-compose-app.yml up

# 6. Wait for startup (30-60 seconds)
# Then access:
# - Frontend: http://localhost:8501
# - API: http://localhost:8000/docs
# - Endee: http://localhost:6379
```

### Option 2: Manual Setup (Advanced)

Jump to the **Manual Setup** section below.

---

## 📋 Prerequisites

### Required
- Python 3.10+ 
- Docker & Docker Compose (for Option 1)
- OpenAI API Key ([get free one](https://platform.openai.com/api-keys))

### Optional
- Git
- curl (for testing)
- A web browser (for UI access)

---

## 📖 Detailed Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/abhishek-p-r/endee.git
cd endee
```

### Step 2: Configure Environment

```bash
# Copy example environment
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your favorite editor
```

**Minimum Required in `.env`:**
```env
OPENAI_API_KEY=sk-your-api-key-here
ENDEE_URL=http://localhost:6379
API_URL=http://localhost:8000
```

### Step 3: Prepare Data (Optional)

```bash
# Create data directory
mkdir -p data

# Add your documents
# - Place .txt files (plain text)
# - Place .pdf files (PDF documents)
# - Place .md files (Markdown)
```

Example file structure:
```
data/
├── document1.txt
├── research_paper.pdf
├── notes.md
└── another_doc.txt
```

---

## 🐳 Docker Compose Setup (Easiest)

### Step 1: Start Services

```bash
docker-compose -f docker-compose-app.yml up
```

### Step 2: Monitor Startup

Watch for these messages:
```
endee-db      | Starting Endee Vector Database...
endee-backend | Starting FastAPI server on 0.0.0.0:8000
endee-frontend| Streamlit running on http://0.0.0.0:8501
```

### Step 3: Access Services

Once all containers show "healthy":

- **Web UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health
- **Endee Health**: http://localhost:6379/health

### Step 4: Ingest Documents

**Via Web UI**:
1. Go to http://localhost:8501
2. Click upload button in sidebar
3. Select document (TXT, PDF, or MD)
4. Click "Process Document"

**Via API**:
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@data/sample.txt"
```

### Step 5: Ask Questions

1. Go to http://localhost:8501
2. Go to "Chat" tab
3. Type your question
4. System searches and answers

---

## 🖥️ Manual Setup (Without Docker)

### Step 1: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate      # Windows
```

### Step 2: Install Dependencies

```bash
pip install -r requirements_new.txt
```

### Step 3: Start Endee Server

**Option A: Docker (just Endee)**
```bash
docker run -p 6379:6379 endeeio/endee:latest
```

**Option B: Local Installation**
Follow [Endee installation guide](https://github.com/endee-io/endee#installation)

### Step 4: Ingest Documents

```bash
cd backend_v2

# Run ingestion script
python ingest_documents.py
```

Example output:
```
INFO - Found 3 documents
INFO - Processing: document1.txt
INFO - Created 15 chunks
INFO - Stored 15 vectors in Endee
...
==================================================
INGESTION REPORT
==================================================
Status: ✓ Success
Documents Ingested: 3
Failed: 0
==================================================
```

### Step 5: Start Backend

```bash
cd backend_v2
python main.py
```

Output:
```
INFO - Starting FastAPI server on 0.0.0.0:8000
INFO - Uvicorn running on http://localhost:8000
INFO - Endee connection established ✓
INFO - RAG pipeline initialized ✓
```

### Step 6: Start Frontend (New Terminal)

```bash
cd frontend_v2
streamlit run app.py
```

Output:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Step 7: Access the Application

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## 🧪 Testing the System

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "endee_connected": true,
  "timestamp": "2024-01-20T10:30:00"
}
```

### Test 2: Collection Statistics

```bash
curl http://localhost:8000/stats
```

Expected response:
```json
{
  "status": "success",
  "collection_stats": {
    "count": 150,
    "memory_used_mb": 25,
    "last_updated": "2024-01-20T10:30:00"
  }
}
```

### Test 3: Simple Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What information is in my documents?",
    "top_k": 5
  }'
```

Expected: Answer based on your documents with sources

### Test 4: Via Streamlit UI

1. Open http://localhost:8501
2. Type a question in the chat
3. See answer + sources + metrics

---

## 📊 Monitoring

### View Logs

**Docker**:
```bash
docker-compose -f docker-compose-app.yml logs -f backend
docker-compose -f docker-compose-app.yml logs -f frontend
```

**Manual**:
```bash
tail -f logs/app.log
```

### Monitor Endee

```bash
# Check Endee health
curl http://localhost:6379/health

# Get collection stats
curl http://localhost:8000/stats
```

### Monitor API

```bash
# API health
curl http://localhost:8000/health

# Check API docs
curl http://localhost:8000/openapi.json
```

---

## 🔧 Configuration Options

### Change API Port

In `.env`:
```env
PORT=8001
```

Or via command line:
```bash
python -m backend_v2.main --port 8001
```

### Change Streamlit Port

In `.env`:
```env
STREAMLIT_SERVER_PORT=8502
```

### Adjust RAG Parameters

In `.env`:
```env
RAG_TOP_K=10           # Number of documents to retrieve
RAG_TEMPERATURE=0.5    # Lower = more focused, Higher = more creative
RAG_MAX_TOKENS=2000    # Maximum answer length
```

### Change Document Chunking

In `.env`:
```env
CHUNK_SIZE=1024        # Larger chunks = fewer but longer
CHUNK_OVERLAP=100      # Overlap between chunks
```

---

## 🚫 Troubleshooting

### Problem: "Connection refused" for Endee

**Solution**: Make sure Endee is running
```bash
# If using Docker:
docker ps | grep endee

# If using local Endee, start it first:
# See Endee documentation
```

### Problem: "Invalid API key" for OpenAI

**Solution**: Check your API key in `.env`
```bash
# Get new key from: https://platform.openai.com/api-keys
# Make sure it starts with: sk-
```

### Problem: Empty search results

**Solution**: 
1. Check documents were ingested
2. Verify Endee has vectors: `curl http://localhost:8000/stats`
3. Try simpler query
4. Increase `RAG_TOP_K`

### Problem: Slow responses

**Solution**:
1. Reduce `RAG_TOP_K` (fewer documents = faster)
2. Use smaller `CHUNK_SIZE` (fewer vectors to search)
3. Check API rate limits
4. Verify network latency

### Problem: High memory usage

**Solution**:
1. Reduce `RAG_TOP_K`
2. Reduce `CHUNK_SIZE`
3. Delete old uploads: `rm -rf uploads/*`
4. Clear cache: `curl -X POST http://localhost:8000/cache/clear`

---

## 📈 Performance Tips

### For Faster Responses
```env
RAG_TOP_K=3                    # Fewer documents
CHUNK_SIZE=1024                # Larger chunks
OPENAI_MODEL=gpt-3.5-turbo     # Faster model
```

### For Better Quality
```env
RAG_TOP_K=10                   # More documents
CHUNK_SIZE=512                 # Smaller chunks (more detail)
OPENAI_MODEL=gpt-4             # More capable model
RAG_TEMPERATURE=0.5            # More focused
```

### For Lower Cost
```env
OPENAI_EMBEDDING_MODEL=text-embedding-3-small   # Cheaper embeddings
OPENAI_MODEL=gpt-3.5-turbo                      # Cheaper LLM
RAG_TOP_K=3                                      # Fewer calls
```

---

## 🗑️ Cleanup

### Stop All Services

**Docker**:
```bash
docker-compose -f docker-compose-app.yml down
```

**Manual**: Press `Ctrl+C` in each terminal

### Remove Data

```bash
# Remove ingested vectors
docker-compose -f docker-compose-app.yml down -v

# Or manually:
rm -rf data/* uploads/* logs/*
```

### Reset Everything

```bash
# Stop and remove everything
docker-compose -f docker-compose-app.yml down -v

# Rebuild
docker-compose -f docker-compose-app.yml build --no-cache
```

---

## 📚 Next Steps

1. ✅ **Run**: Start the application
2. ✅ **Ingest**: Add your documents
3. ✅ **Query**: Ask questions
4. ✅ **Monitor**: Check stats and health
5. ✅ **Deploy**: Move to production

---

## 🎯 Common Workflows

### Workflow 1: Quick Testing

```bash
# Start services
docker-compose -f docker-compose-app.yml up

# Wait for startup
sleep 30

# Test health
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### Workflow 2: Production Deployment

```bash
# Build images
docker-compose -f docker-compose-app.yml build

# Start in background
docker-compose -f docker-compose-app.yml up -d

# Monitor logs
docker-compose -f docker-compose-app.yml logs -f

# Scale if needed
docker-compose -f docker-compose-app.yml up -d --scale backend=2
```

### Workflow 3: Document Ingestion

```bash
# Start system
docker-compose -f docker-compose-app.yml up -d

# Wait for healthy
sleep 30

# Upload documents via API
for file in data/*.txt; do
  curl -X POST http://localhost:8000/documents/upload \
    -F "file=@$file"
done

# Or use Web UI
# Go to http://localhost:8501 and upload
```

---

## 💡 Pro Tips

- **Save costs**: Use `gpt-3.5-turbo` instead of `gpt-4`
- **Faster responses**: Reduce `RAG_TOP_K` from 5 to 3
- **Better answers**: Increase `CHUNK_OVERLAP`
- **Monitor performance**: Check `/stats` endpoint regularly
- **Debug queries**: Use `/query/retrieve` to see what was found
- **Scale API**: Run multiple backend instances

---

## 📞 Support

If issues occur:
1. Check logs: `docker-compose logs`
2. Verify health: `curl http://localhost:8000/health`
3. Check Endee: `curl http://localhost:6379/health`
4. Review [README_PRODUCTION.md](./README_PRODUCTION.md)
5. Check [troubleshooting section](#-troubleshooting)

---

**You're all set! Happy knowledge assistance! 🎉**

Last Updated: January 2024
