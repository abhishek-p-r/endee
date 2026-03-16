# How to Run Endee AI Knowledge Assistant

A complete guide to getting the Endee AI Knowledge Assistant up and running on your system.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Detailed Setup](#detailed-setup)
4. [Running the Application](#running-the-application)
5. [Accessing the Services](#accessing-the-services)
6. [Ingesting Documents](#ingesting-documents)
7. [Testing the System](#testing-the-system)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Configuration](#advanced-configuration)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB for dependencies and documents
- **OS**: Linux, macOS, or Windows (WSL2 recommended for Windows)

### Required API Keys
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))
  - Free tier available with 60 requests/minute limit
  - Sign up at: https://ai.google.dev

### Optional Components
- **Docker** (for containerized deployment)
- **Endee Vector Database** (if not using in-memory fallback)

---

## Quick Start (5 minutes)

For the fastest setup, use the automated script:

### Step 1: Navigate to Project Directory
```bash
cd endee-ai-knowledge-assistant
```

### Step 2: Run the Startup Script
```bash
# Make script executable (macOS/Linux only)
chmod +x start.sh

# Run the startup script
./start.sh
```

### Step 3: Configure API Key
When prompted:
```bash
Enter your Google Gemini API Key: [paste_your_key_here]
```

Get your free API key at: https://makersuite.google.com/app/apikey

### Step 4: Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000/docs

**Done!** You're ready to start asking questions. 🎉

---

## Detailed Setup

### Step 1: Clone or Extract Project

If you don't have the project yet:

```bash
# Using git
git clone https://github.com/abhishek-p-r/endee.git
cd endee

# Or if you have a ZIP file
unzip endee-ai-knowledge-assistant.zip
cd endee-ai-knowledge-assistant
```

### Step 2: Create Python Virtual Environment

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Verify Python Version

```bash
python --version  # Should be 3.9+
```

Expected output:
```
Python 3.9.0  # (or higher)
```

### Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (backend server)
- Streamlit (frontend UI)
- Sentence Transformers (embeddings)
- google-generativeai (Gemini API)
- And other dependencies

**Installation takes 2-3 minutes.**

### Step 5: Create Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env
```

**On Windows (Command Prompt):**
```cmd
copy .env.example .env
```

### Step 6: Add Your API Keys

Edit the `.env` file and add your credentials:

```bash
# Using nano (macOS/Linux)
nano .env

# Using vi (macOS/Linux)
vi .env

# On Windows, use any text editor
notepad .env
```

Required configuration:
```env
# REQUIRED: Your Google Gemini API key
GEMINI_API_KEY=your_api_key_here_from_makersuite

# OPTIONAL: Endee vector database URL (defaults to in-memory)
ENDEE_URL=http://localhost:8080

# OPTIONAL: Customize embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# OPTIONAL: Logging level
LOG_LEVEL=INFO
```

Save the file (Ctrl+X, then Y, then Enter if using nano).

---

## Running the Application

### Option A: Using Automated Startup Script (Recommended)

The easiest way to start everything:

```bash
# Make script executable (first time only)
chmod +x start.sh

# Run the script
./start.sh
```

The script will:
1. Create necessary directories (`logs/`, `data/`, `documents/`)
2. Start the FastAPI backend (port 8000)
3. Start the Streamlit frontend (port 8501)
4. Ask if you want to ingest sample documents
5. Open the browser automatically

**To stop the application:** Press `Ctrl+C` in the terminal

---

### Option B: Manual Startup in Separate Terminals

Gives you more control and visibility:

#### Terminal 1 - Backend Server

```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start the FastAPI backend
python -m uvicorn backend.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Terminal 2 - Frontend UI

Open a new terminal in the same project directory:

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start Streamlit
streamlit run frontend/streamlit_app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

#### Terminal 3 - Optional: Ingest Sample Documents

To load sample documents on first run:

```bash
# Activate virtual environment
source venv/bin/activate

# Ingest sample documents
python -m scripts.ingest_documents --mode sample
```

Expected output:
```
[INFO] Loading sample documents...
[INFO] Processed: vector_databases.md
[INFO] Processed: embeddings_guide.md
[INFO] Total chunks ingested: 45
```

---

### Option C: Docker Deployment

For containerized deployment:

#### Prerequisites
- Docker installed ([Get Docker](https://www.docker.com/products/docker-desktop))

#### Steps

```bash
# Navigate to project directory
cd endee-ai-knowledge-assistant

# Build and start services
docker-compose -f docker-compose-app.yml up

# On first run, it will:
# - Build the Docker image
# - Start FastAPI backend
# - Start Streamlit frontend
# - Create volumes for persistence
```

Expected output:
```
backend_1    | INFO:     Uvicorn running on http://0.0.0.0:8000
streamlit_1  | Local URL: http://localhost:8501
```

To stop:
```bash
docker-compose -f docker-compose-app.yml down
```

To view logs:
```bash
docker-compose -f docker-compose-app.yml logs -f
```

---

## Accessing the Services

### Web Interface (Streamlit)

Open your browser and navigate to:
```
http://localhost:8501
```

**You will see:**
- Chat interface on the left
- Sidebar with upload and settings on the right
- Message history
- Response details toggle

### Backend API Documentation

Open your browser and navigate to:
```
http://localhost:8000/docs
```

You can:
- View all available API endpoints
- Test endpoints directly
- See request/response schemas
- Understand parameter requirements

Alternative documentation:
```
http://localhost:8000/redoc
```

### Health Check

Verify the backend is running:

```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "2024-03-16T10:30:00"}
```

---

## Ingesting Documents

### Option 1: Web UI Upload (Easiest)

1. Open http://localhost:8501
2. Click **"📚 Document Upload"** in the sidebar
3. Select a file (PDF, TXT, or Markdown)
4. Click **"📤 Upload & Ingest"**
5. Wait for confirmation: "✅ Documents ingested successfully"

Supported formats:
- PDF (.pdf)
- Plain Text (.txt)
- Markdown (.md)

### Option 2: Command Line

**Ingest sample documents:**
```bash
python -m scripts.ingest_documents --mode sample
```

**Ingest a single file:**
```bash
python -m scripts.ingest_documents --mode file --path path/to/document.pdf
```

**Ingest entire directory:**
```bash
python -m scripts.ingest_documents --mode directory --path ./my_documents
```

**Ingest with custom source name:**
```bash
python -m scripts.ingest_documents --mode file --path doc.txt --source "My Custom Source"
```

### Option 3: API Endpoint

```bash
# Upload document via API
curl -X POST http://localhost:8000/upload \
  -F "file=@path/to/document.pdf"

# Expected response:
# {"status": "success", "chunks": 25, "tokens": 3500}
```

---

## Testing the System

### Test 1: Basic Health Check

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2024-03-16T10:30:00"
}
```

### Test 2: Ask a Question via API

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is a vector database?",
    "session_id": "test-session",
    "top_k": 5
  }'
```

Expected response:
```json
{
  "answer": "A vector database is...",
  "sources": [
    {
      "content": "...",
      "source": "vector_databases.md",
      "chunk_id": "chunk_0"
    }
  ],
  "query_analysis": {
    "original": "What is a vector database?",
    "optimized": "explain vector database concept definition"
  }
}
```

### Test 3: Using the Web UI

1. Open http://localhost:8501
2. Ask a question: "Tell me about embeddings"
3. You should see:
   - The AI's answer
   - Source documents
   - Response time
   - Query analysis details

### Test 4: Document Upload

1. Download a sample document or use a PDF
2. In the sidebar, click "📚 Document Upload"
3. Select the file
4. Click "📤 Upload & Ingest"
5. Confirm success message

---

## Troubleshooting

### Issue: "Port 8000 is already in use"

**Problem:** FastAPI backend can't start because port 8000 is occupied

**Solutions:**

Option 1: Use a different port
```bash
python -m uvicorn backend.main:app --port 8001
```

Option 2: Kill the process using port 8000

**macOS/Linux:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Windows (Command Prompt):**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Windows (PowerShell):**
```powershell
Get-NetTCPConnection -LocalPort 8000
Stop-Process -Id <PID> -Force
```

---

### Issue: "ModuleNotFoundError: No module named..."

**Problem:** Python dependencies not installed

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Or upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Issue: "Streamlit won't load at localhost:8501"

**Problem:** Streamlit frontend not starting properly

**Solutions:**

Option 1: Run with debug mode
```bash
streamlit run frontend/streamlit_app.py --logger.level=debug
```

Option 2: Clear Streamlit cache
```bash
streamlit cache clear
streamlit run frontend/streamlit_app.py
```

Option 3: Update Streamlit
```bash
pip install --upgrade streamlit
streamlit run frontend/streamlit_app.py
```

---

### Issue: "GEMINI_API_KEY is not set"

**Problem:** API key is missing or not configured

**Solution:**

1. Get a free API key at: https://makersuite.google.com/app/apikey
2. Edit `.env` file:
   ```bash
   nano .env  # or use your editor
   ```
3. Add your key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
4. Save and restart the application

**Verify:**
```bash
echo $GEMINI_API_KEY  # macOS/Linux
echo %GEMINI_API_KEY%  # Windows Command Prompt
$env:GEMINI_API_KEY  # Windows PowerShell
```

---

### Issue: "Connection refused - Endee not running"

**Problem:** Backend can't connect to Endee vector database

**This is not critical** - the system has an in-memory fallback

**Option 1: Use in-memory mode (default)**
- No action needed
- System will use in-memory vector search
- Performance is fine for up to 1000 documents

**Option 2: Run Endee separately**

```bash
# Clone Endee repository
git clone https://github.com/endee-io/endee.git
cd endee

# Install and build
chmod +x install.sh run.sh
./install.sh --release --avx2

# Run Endee server
./run.sh

# It will start on http://localhost:8080

# In another terminal, restart your app:
./start.sh
```

---

### Issue: "API Response is slow"

**Reasons and Solutions:**

1. **Large documents being processed**
   - Reduce chunk size in config.py
   - Increase top_k results retrieval

2. **Low system resources**
   - Close other applications
   - Increase RAM allocation if using Docker
   - Reduce number of concurrent requests

3. **Embedding model is slow**
   - Check EMBEDDING_MODEL in .env
   - Default `all-MiniLM-L6-v2` is optimized for speed

4. **First request takes longer**
   - Models are loaded on first request
   - Subsequent requests will be faster

---

### Issue: "PDF extraction fails"

**Problem:** PDFs aren't being processed correctly

**Solution:**

Check if PDF is text-based (not scanned):
```bash
# Test with a known good PDF first
python -m scripts.ingest_documents --mode file --path test.pdf
```

If scanned PDF, use OCR (requires additional setup):
```bash
# Install OCR support
pip install pytesseract pdf2image

# Then try again
python -m scripts.ingest_documents --mode file --path scanned.pdf
```

---

## Advanced Configuration

### Custom Embedding Model

Edit `backend/config.py`:

```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Change to another model
```

Available models:
- `all-MiniLM-L6-v2` (Fast, recommended)
- `all-MiniLM-L12-v2` (More accurate)
- `sentence-transformers/paraphrase-MiniLM-L6-v2`

### Customize Chunk Size

Edit `backend/config.py`:

```python
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100  # Overlap between chunks
```

- Smaller chunks = more precise but more requests
- Larger chunks = fewer requests but less precise

### Adjust RAG Parameters

Edit `backend/rag_pipeline.py`:

```python
top_k = 5  # Number of sources to retrieve
max_tokens = 2000  # Max response length
temperature = 0.7  # Creativity of response (0.0-1.0)
```

### Configure Logging

Edit `.env`:

```env
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

View logs:
```bash
tail -f logs/app_*.log
```

### Enable CORS for External Access

Edit `backend/main.py` and update:

```python
origins = [
    "http://localhost:3000",  # Add your frontend URL
    "https://yourdomain.com",
]
```

---

## Performance Optimization

### For Production Use

1. **Use Endee Vector Database** (instead of in-memory)
   - Better performance for large document sets
   - Persistent storage

2. **Enable Caching**
   ```python
   # In backend/main.py
   CACHE_RESPONSES = True
   CACHE_TTL = 3600  # 1 hour
   ```

3. **Use Async Processing**
   - Already enabled by default
   - Handles multiple concurrent requests

4. **Monitor Logs**
   ```bash
   tail -f logs/app_*.log
   ```

---

## Next Steps After Setup

1. **Ingest Your Documents**
   - Use web UI or command line
   - Support for PDF, TXT, Markdown

2. **Customize the System**
   - Edit prompts in `backend/bots/`
   - Adjust RAG parameters
   - Configure embedding model

3. **Deploy to Production**
   - Use Docker for consistency
   - Set up monitoring
   - Configure authentication if needed

4. **Read Full Documentation**
   - `AI_KNOWLEDGE_ASSISTANT_README.md` - Complete reference
   - `DEVELOPMENT.md` - Architecture details
   - `PROJECT_STRUCTURE.md` - File organization

---

## Getting Help

- **API Issues?** Check `http://localhost:8000/docs`
- **Can't start?** Check the Troubleshooting section above
- **Want to customize?** See `DEVELOPMENT.md`
- **Full documentation?** Read `AI_KNOWLEDGE_ASSISTANT_README.md`
- **Questions about Endee?** Visit [endee.io](https://endee.io/)

---

## Summary

You now have a fully functional Endee AI Knowledge Assistant! Here's what you can do:

✅ Ask questions about your documents
✅ Upload new documents anytime
✅ Get AI-powered answers with source attribution
✅ Maintain conversation history
✅ Scale to thousands of documents

**Start with the Quick Start section if you haven't already!**

---

**Happy questioning!** 🚀
