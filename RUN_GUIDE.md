# Complete Guide to Running Endee AI Knowledge Assistant

## Table of Contents
1. [Quick Start (5 minutes)](#quick-start)
2. [Detailed Setup](#detailed-setup)
3. [Running the Application](#running-the-application)
4. [Docker Deployment](#docker-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional, for Endee database)
- Google Gemini API Key (free)

### Step 1: Get Gemini API Key (2 minutes)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### Step 2: Setup Endee Database (3 minutes)

**Option A: Using Docker (Easiest)**
```bash
docker run -d -p 8080:8080 endeeio/endee:latest
```

**Option B: From Source**
```bash
git clone https://github.com/endee-io/endee.git
cd endee
chmod +x install.sh run.sh
./install.sh --release --avx2
./run.sh
```

Verify Endee is running:
```bash
curl http://localhost:8080/health
# Should return 200 OK
```

### Step 3: Install Dependencies (2 minutes)
```bash
cd /path/to/endee-ai-knowledge-assistant
pip install -r requirements.txt
```

### Step 4: Configure Environment (1 minute)
```bash
cp .env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY=your_api_key_here
ENDEE_URL=http://localhost:8080
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True
```

### Step 5: Run the Application
```bash
# Start backend
python -m uvicorn backend.main:app --reload --port 8000

# In another terminal, start frontend
streamlit run frontend/streamlit_enhanced.py
```

**Frontend will be available at:** http://localhost:8501

---

## Detailed Setup

### 1. Clone Repository
```bash
git clone https://github.com/abhishek-p-r/endee.git
cd endee-ai-knowledge-assistant
```

### 2. Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Check installation:
```bash
python -c "import fastapi; import streamlit; print('✓ All packages installed')"
```

### 4. Setup Environment Variables

Create `.env` file:
```bash
cat > .env << EOF
# AI Configuration
GEMINI_API_KEY=your_api_key_from_step_1

# Endee Database
ENDEE_URL=http://localhost:8080
ENDEE_COLLECTION_NAME=knowledge_base

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RETRIEVAL_LIMIT=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
EOF
```

### 5. Verify Endee Connection
```bash
python scripts/test_api.py
```

This will:
- Test Endee database connectivity
- Verify Gemini API access
- Check all system components

---

## Running the Application

### Method 1: Automated Script (Easiest)
```bash
chmod +x start.sh
./start.sh
```

This script will:
1. Check dependencies
2. Start Endee (if not running)
3. Start FastAPI backend
4. Start Streamlit frontend
5. Open browser to UI

### Method 2: Manual Command (Step-by-Step)

**Terminal 1 - Start FastAPI Backend:**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Output should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
✓ Endee vector database is connected
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run frontend/streamlit_enhanced.py
```

Output should show:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your-ip:8501
```

**Terminal 3 (Optional) - Check Endee:**
```bash
curl http://localhost:8080/health
```

Should return:
```json
{"status": "healthy"}
```

### Access Points
- **Frontend UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Endee Database**: http://localhost:8080

---

## Docker Deployment

### Option 1: Docker Compose (Full Stack)

```bash
docker-compose -f docker-compose-app.yml up
```

This starts:
- Endee vector database (port 8080)
- FastAPI backend (port 8000)
- Streamlit frontend (port 8501)

Access:
- Frontend: http://localhost:8501
- API: http://localhost:8000/docs

### Option 2: Build Custom Image

```bash
# Build image
docker build -t endee-ai-assistant:latest .

# Run container
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e ENDEE_URL=http://endee:8080 \
  endee-ai-assistant:latest
```

---

## Running with Your Documents

### Method 1: Upload via UI
1. Open http://localhost:8501
2. Go to sidebar → "Document Management"
3. Upload PDF/TXT/MD file
4. Click "Ingest Document"
5. Start asking questions

### Method 2: Batch Ingest
```bash
python scripts/ingest_documents.py \
  --input-dir ./data/documents \
  --file-types pdf txt md
```

### Method 3: API Call
```bash
curl -X POST http://localhost:8000/ingest/upload \
  -F "file=@document.pdf" \
  -F "source=my_document"
```

---

## Testing the System

### 1. Quick Test
```bash
python scripts/test_api.py
```

### 2. Manual API Test
```bash
# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "session_id": "test_session",
    "use_conversation_history": true
  }'
```

### 3. Upload Test File
```bash
# Create test file
echo "Machine learning is a subset of artificial intelligence." > test.txt

# Upload
curl -X POST http://localhost:8000/ingest/upload \
  -F "file=@test.txt" \
  -F "source=test_document"
```

---

## Troubleshooting

### Issue: "Connection refused to Endee"
**Solution:**
```bash
# Check if Endee is running
curl http://localhost:8080/health

# If not, start it:
docker run -d -p 8080:8080 endeeio/endee:latest
```

### Issue: "GEMINI_API_KEY not found"
**Solution:**
1. Edit `.env` file
2. Add your API key: `GEMINI_API_KEY=your_actual_key`
3. Restart backend

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Change port in .env
SERVER_PORT=8001

# Or kill existing process
lsof -i :8000
kill -9 <PID>
```

### Issue: "No module named 'backend'"
**Solution:**
```bash
# Make sure you're in project root
cd /path/to/endee-ai-knowledge-assistant

# Ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Restart backend
```

### Issue: "Streamlit page is blank"
**Solution:**
```bash
# Clear cache and restart
streamlit cache clear
streamlit run frontend/streamlit_enhanced.py
```

### Issue: "Low retrieval quality"
**Solution:**
1. Upload more documents (at least 5-10)
2. Use specific questions
3. Check query optimization in "Query Optimizer" tab
4. Increase `RETRIEVAL_LIMIT` in `.env`

---

## Performance Optimization

### 1. Enable Caching
- Automatically enabled in enhanced version
- Check cache stats in Analytics tab

### 2. Optimize Chunk Size
Edit `.env`:
```
CHUNK_SIZE=1000      # Larger = fewer chunks, faster retrieval
CHUNK_OVERLAP=100    # Overlap between chunks
```

### 3. Adjust Retrieval Limit
```
RETRIEVAL_LIMIT=10   # More results = slower but more comprehensive
```

### 4. Use Query Optimization
- Use "Query Optimizer" tab before asking
- Validates query and suggests improvements

---

## Monitoring

### View System Analytics
1. Open http://localhost:8501
2. Go to "Analytics" tab
3. View:
   - Total queries processed
   - Success rate
   - Average response time
   - Cache performance
   - Recent queries

### API Endpoints Summary
```
GET  /health                    - Health check
POST /ask                       - Ask question
POST /ingest                    - Ingest documents
POST /ingest/upload            - Upload files
GET  /analytics/stats          - Get analytics
GET  /analytics/report         - Full report
GET  /query/optimize           - Analyze query
POST /cache/clear              - Clear cache
GET  /chat/history/{session_id} - Get chat history
DELETE /chat/history/{session_id} - Clear history
```

---

## Common Workflows

### Workflow 1: Start Fresh
```bash
# 1. Start Endee
docker run -d -p 8080:8080 endeeio/endee:latest

# 2. Start backend
python -m uvicorn backend.main:app --reload

# 3. Start frontend
streamlit run frontend/streamlit_enhanced.py

# 4. Upload documents via UI
# 5. Ask questions
```

### Workflow 2: Production Deployment
```bash
# 1. Build Docker image
docker build -t endee-ai-prod:latest .

# 2. Run with docker-compose
docker-compose -f docker-compose-app.yml up -d

# 3. Monitor logs
docker-compose logs -f
```

### Workflow 3: Development
```bash
# 1. Activate venv
source venv/bin/activate

# 2. Run with auto-reload
./start.sh

# 3. Code changes auto-reload
# 4. Test via http://localhost:8501
```

---

## Next Steps

1. **Upload Documents**: Add your knowledge base
2. **Ask Questions**: Test with natural language queries
3. **Monitor Performance**: Check Analytics tab
4. **Optimize Queries**: Use Query Optimizer
5. **Review Responses**: Check Retrieved Sources
6. **Scale Up**: Deploy to production with Docker

---

## Support

For issues:
1. Check [TROUBLESHOOTING](#troubleshooting) section
2. Review logs in `/logs` directory
3. Check API docs at http://localhost:8000/docs
4. See full documentation in `/docs` folder

---

**Happy Knowledge Assistance! 🚀**
