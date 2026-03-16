# Complete Setup & Run Guide - Endee AI Knowledge Assistant

This guide provides **step-by-step instructions** to get the system running from scratch.

## Quick Summary

This is a **RAG (Retrieval Augmented Generation)** system that:
1. Loads documents from `.txt` files
2. Converts them to embeddings (vector representations)
3. Stores embeddings in **Endee Vector Database**
4. Retrieves relevant documents when you ask questions
5. Uses Google Gemini AI to generate answers

**Time Required**: 15-20 minutes for complete setup

---

## Part 1: Prerequisites Check

### Required Software
```bash
# Python 3.8 or higher
python --version

# Git
git --version

# pip (comes with Python)
pip --version
```

If any are missing, install them:
- Python: https://www.python.org/downloads/
- Git: https://git-scm.com/downloads/

### Hardware Requirements
- CPU: Any modern processor
- RAM: 4GB minimum (8GB recommended)
- Disk: 2GB free space
- Network: Internet connection (for Gemini API)

---

## Part 2: Get the Code

### Clone the Repository
```bash
# Navigate to where you want the project
cd ~/projects  # or your preferred location

# Clone the repository
git clone https://github.com/abhishek-p-r/endee.git
cd endee

# Switch to AI assistant branch
git checkout endee-ai-assistant
```

### Verify Project Structure
```bash
# You should see these directories:
ls -la

# Expected output:
# backend/              (FastAPI application)
# frontend/             (Streamlit UI)
# scripts/              (ingestion utilities)
# data/                 (documents go here)
# requirements.txt
# .env.example
```

---

## Part 3: Set Up Python Environment

### Create Virtual Environment
```bash
# Create venv (recommended for isolation)
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# After activation, you should see (venv) in your terminal
```

### Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will install:
# - fastapi, uvicorn (API server)
# - streamlit (Web UI)
# - sentence-transformers (embeddings)
# - google-generativeai (Gemini)
# - httpx (Endee client)
# - And more...

# Verify installation
pip list | grep -E "fastapi|streamlit|sentence-transformers"
```

---

## Part 4: Set Up Endee Vector Database

### Option A: Local Installation (Linux/macOS)

**Step 1: Navigate to Endee Directory**
```bash
# The Endee source code is already in the repo
cd endee

# If it's a separate clone:
git clone https://github.com/endee-io/endee.git
cd endee
```

**Step 2: Install Endee**
```bash
# Make scripts executable
chmod +x install.sh run.sh

# Install Endee (this will download prebuilt binary)
./install.sh --release --avx2

# You should see:
# Downloading Endee binary...
# Installation complete!
```

**Step 3: Run Endee Server**
```bash
# Start the Endee server
./run.sh

# You should see:
# Starting Endee server...
# Server listening on http://localhost:8080

# Keep this terminal open! Endee needs to stay running
```

**Step 4: Verify Endee is Running**
```bash
# In a new terminal, test the connection:
curl http://localhost:8080/health

# Should return:
# {"status": "healthy"}
```

### Option B: Docker (Recommended for Windows/Mac)

**Using Docker Compose (Easiest)**
```bash
# From the project root directory
docker-compose -f docker-compose-app.yml up endee-db

# This will:
# 1. Build the Endee image
# 2. Start Endee on port 8080
# 3. Keep running in background

# Verify:
curl http://localhost:8080/health
```

**Manual Docker**
```bash
# Build image
docker build -f Dockerfile.endee -t endee-db .

# Run container
docker run -p 8080:8080 endee-db

# The Endee server will be available at http://localhost:8080
```

---

## Part 5: Configure Application

### Create Environment File
```bash
# Go back to project root
cd ..  # if you're in endee/

# Copy the example config
cp .env.example .env

# Edit the file with your settings
nano .env  # or use your preferred editor
```

### Configure .env File

**Essential Configuration:**
```env
# Endee Vector Database
ENDEE_URL=http://localhost:8080
ENDEE_COLLECTION_NAME=knowledge_base

# Google Gemini AI (REQUIRED)
GEMINI_API_KEY=your_api_key_here

# Optional: Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Optional: Server Ports
BACKEND_PORT=8000
STREAMLIT_PORT=8501

# Optional: Logging
LOG_LEVEL=INFO
```

### Get Google Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste into `.env` file as `GEMINI_API_KEY=your_key_here`

**It's free to get started!** You get 60 requests per minute.

---

## Part 6: Prepare Your Documents

### Create Data Directory
```bash
# Create a directory for documents (if not exists)
mkdir -p data

# You can add your own .txt files here
```

### Add Sample Documents (Optional)
The system will create sample documents automatically if you don't add any. These samples include:
- endee_guide.txt - Information about Endee
- embeddings_guide.txt - How embeddings work
- rag_systems.txt - RAG explanation

### Add Your Own Documents
```bash
# Copy your .txt files to data/
cp /path/to/your/documents/*.txt data/

# Example:
# data/company_handbook.txt
# data/product_documentation.txt
# data/faqs.txt
```

---

## Part 7: Ingest Documents Into Endee

### Run the Ingestion Script

**In a new terminal:**
```bash
# Activate venv first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run ingestion
python scripts/ingest_documents.py

# You should see output like:
# Verifying Endee connection...
# ✓ Successfully connected to Endee server
# Creating/Verifying collection...
# ✓ Collection 'knowledge_base' ready
# Loading documents from data/...
# ✓ Loaded 3 documents
# Processing documents into chunks...
#   endee_guide.txt: 4 chunks
#   embeddings_guide.txt: 5 chunks
#   rag_systems.txt: 4 chunks
# ✓ Created 13 chunks from 3 documents
# Generating embeddings for 13 chunks...
# ✓ Generated 13 embeddings in 2.34s
# Upserting 13 vectors to Endee...
#   ✓ Batch 1: 13 vectors (0.45s)
# ✓ Upsert complete: 13 successful, 0 failed
#
# ===== PIPELINE SUMMARY =====
# Status: completed
# Documents loaded: 3
# Chunks created: 13
# Embeddings generated: 13
# Vectors stored: 13
```

### Verify Ingestion
```bash
# Check Endee has the data
curl http://localhost:8080/collections

# Should show your collection with vectors
```

---

## Part 8: Start the Backend API

### In a new terminal:
```bash
# Activate venv
source venv/bin/activate  # or venv\Scripts\activate

# Start FastAPI server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# You should see:
# Uvicorn running on http://0.0.0.0:8000
# Application startup complete

# The API is now available at:
# - REST API: http://localhost:8000
# - Swagger UI: http://localhost:8000/docs
```

### Test the API
```bash
# In another terminal, test an endpoint
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Endee?", "session_id": "test"}'

# You should get a JSON response with an answer!
```

---

## Part 9: Start the Streamlit Web UI

### In a new terminal:
```bash
# Activate venv
source venv/bin/activate

# Start Streamlit
streamlit run frontend/streamlit_app.py

# You should see:
# You can now view your Streamlit app in your browser
# Local URL: http://localhost:8501
# Network URL: http://your-ip:8501

# Browser should open automatically
```

---

## Part 10: Test the Complete System

### Via Web UI (Easiest)
1. Browser opens to http://localhost:8501
2. You see a chat interface
3. Type a question: "What is Endee?"
4. Click Send or press Enter
5. Get an AI-powered answer with sources!

### Via API (for Integration)
```bash
# Ask a question
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do embeddings work?",
    "session_id": "user1"
  }'

# Get analytics
curl http://localhost:8000/analytics/stats

# Optimize a query
curl -X POST "http://localhost:8000/query/optimize" \
  -d "question=what%20is%20a%20vector%20database"
```

---

## Complete Terminal Setup (All at Once)

If you want to see it all running:

**Terminal 1: Endee Server**
```bash
cd endee
./run.sh
# Keep running
```

**Terminal 2: Ingest Documents**
```bash
source venv/bin/activate
python scripts/ingest_documents.py
# Wait for completion
```

**Terminal 3: Backend API**
```bash
source venv/bin/activate
python -m uvicorn backend.main:app --reload --port 8000
# Keep running
```

**Terminal 4: Streamlit UI**
```bash
source venv/bin/activate
streamlit run frontend/streamlit_app.py
# Automatic browser open
```

**Terminal 5: Testing (Optional)**
```bash
# Test the system
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about Endee"}'
```

---

## Troubleshooting

### Issue 1: "Connection to Endee failed"
```
Error: Cannot connect to http://localhost:8080

Solution:
1. Verify Endee is running: curl http://localhost:8080/health
2. If not, start Endee: cd endee && ./run.sh
3. Check .env ENDEE_URL is correct
```

### Issue 2: "GEMINI_API_KEY not found"
```
Error: Environment variable not set

Solution:
1. Get API key: https://makersuite.google.com/app/apikey
2. Add to .env: GEMINI_API_KEY=your_key
3. Restart backend: python -m uvicorn backend.main:app
```

### Issue 3: "No documents found"
```
Error: Empty search results

Solution:
1. Check data/ has .txt files
2. Run ingestion: python scripts/ingest_documents.py
3. Verify ingestion succeeded (13 vectors stored)
4. Restart backend to reload
```

### Issue 4: "Slow responses"
```
First response: 3-5 seconds (normal, model loading)
Subsequent queries: 1-2 seconds (normal)
Cached queries: <500ms

Check analytics: curl http://localhost:8000/analytics/stats
```

### Issue 5: "Port already in use"
```
Error: Address already in use

Solution - Change port in command:
python -m uvicorn backend.main:app --port 8001  # Use 8001 instead
streamlit run frontend/streamlit_app.py --server.port 8502
```

---

## System Architecture Verification

After complete setup, you should have:

```
┌──────────────────────────────────────────────────────────────┐
│ 1. ENDEE SERVER (Port 8080)                                  │
│    Status: http://localhost:8080/health                      │
│    Contains: Embeddings from your documents                  │
└──────────────────────────────────────────────────────────────┘
                              ↑
                              │ queries
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. FASTAPI BACKEND (Port 8000)                               │
│    Endpoints: http://localhost:8000/docs                     │
│    Manages: Query processing, embedding generation           │
└──────────────────────────────────────────────────────────────┘
                              ↑
                              │ HTTP requests
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. STREAMLIT WEB UI (Port 8501)                              │
│    Browser: http://localhost:8501                            │
│    Use: Ask questions and get answers                        │
└──────────────────────────────────────────────────────────────┘
```

---

## What's Next?

### Use the System
- Ask questions via the web UI
- Upload more documents to data/
- Run ingestion again
- Get answers from your knowledge base!

### Customize
- Modify .env for different settings
- Change chunk size in ingest script
- Add custom documents
- Deploy to production

### Monitor
- Check analytics: http://localhost:8000/analytics/stats
- View API docs: http://localhost:8000/docs
- Review logs: Check terminal output

---

## Quick Reference

| Component | Port | Status Check | Purpose |
|-----------|------|--------------|---------|
| Endee DB | 8080 | curl http://localhost:8080/health | Vector storage |
| API | 8000 | curl http://localhost:8000/health | Query processing |
| UI | 8501 | http://localhost:8501 | User interface |

## Common Commands

```bash
# Activate venv
source venv/bin/activate

# Ingest documents
python scripts/ingest_documents.py

# Start backend
python -m uvicorn backend.main:app --reload

# Start UI
streamlit run frontend/streamlit_app.py

# Test API
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question":"test"}'

# View analytics
curl http://localhost:8000/analytics/stats

# Check Endee
curl http://localhost:8080/health
```

---

**Congratulations!** Your Endee AI Knowledge Assistant is now ready to use! 🚀
