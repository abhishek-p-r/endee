# START HERE - Complete Guide to Running Endee AI Assistant

Welcome! This document will help you get started with the Endee AI Knowledge Assistant.

---

## What is This?

An AI-powered assistant that:
- Understands your questions
- Searches through your documents
- Uses Google Gemini to generate intelligent answers
- Shows you which documents it used

---

## Choose Your Path

### Path 1: "Just Get It Running!" (5 minutes)

**For:** People who want to see it working immediately

1. Open a terminal in the project directory
2. Run this one command:

```bash
chmod +x start.sh && ./start.sh
```

3. When asked, enter your Gemini API key (get it free: https://makersuite.google.com/app/apikey)
4. Open http://localhost:8501 in your browser

**Need help?** → See [HOW_TO_RUN.md](./HOW_TO_RUN.md#quick-start-5-minutes)

---

### Path 2: "Step-by-Step Setup" (10-15 minutes)

**For:** People who prefer to understand each step

Follow the detailed guide: [HOW_TO_RUN.md](./HOW_TO_RUN.md)

This covers:
- System requirements
- Virtual environment setup
- Dependency installation
- Configuration
- Running the application
- Troubleshooting

---

### Path 3: "I Prefer Docker" (10 minutes)

**For:** People who want containerized deployment

1. Install Docker if not already: https://www.docker.com/products/docker-desktop
2. In the project directory, run:

```bash
docker-compose -f docker-compose-app.yml up
```

3. Wait for services to start (1-2 minutes)
4. Open http://localhost:8501

**Full Docker instructions** → [HOW_TO_RUN.md#option-c-docker-deployment](./HOW_TO_RUN.md#option-c-docker-deployment)

---

## What You Need Before Starting

### Required
- **Gemini API Key** (FREE tier available)
  - Get it at: https://makersuite.google.com/app/apikey
  - Click "Create API Key"
  - Copy the key

### Choose One:
- **Python 3.9+** (for local setup), OR
- **Docker** (for container setup)

That's all! No database setup required. The system uses in-memory storage by default.

---

## The Quickest Start

Copy and paste this into your terminal:

**macOS/Linux:**
```bash
cd endee-ai-knowledge-assistant
chmod +x start.sh
./start.sh
```

**Windows (Command Prompt):**
```cmd
cd endee-ai-knowledge-assistant
start.sh
```

**Windows (PowerShell):**
```powershell
cd endee-ai-knowledge-assistant
.\start.sh
```

When it asks for your API key, paste the key you got from https://makersuite.google.com/app/apikey

Then visit: http://localhost:8501

---

## First Steps After Starting

### 1. Upload a Document

- Click **"📚 Document Upload"** in the left sidebar
- Select a PDF, TXT, or Markdown file
- Click **"📤 Upload & Ingest"**
- Wait for confirmation

### 2. Ask a Question

- Type in the chat box: "What is this document about?"
- Press Enter
- Wait for the AI response (5-10 seconds)

### 3. View Details

- Click **"📊 Response Details"** to see which documents were used
- Check **"🔍 Query Analysis"** to see how the system understood your question

### 4. Continue the Conversation

- Ask follow-up questions
- Upload more documents
- The system remembers the conversation

---

## Web Addresses to Bookmark

After starting, you can access:

| Address | Purpose |
|---------|---------|
| http://localhost:8501 | **Main Web UI** - Use this to chat |
| http://localhost:8000/docs | API Documentation - For developers |
| http://localhost:8000/redoc | Alternative API Documentation |

---

## How It Works (Simple Version)

```
You Ask a Question
        ↓
System Understands Your Question
        ↓
System Searches Your Documents
        ↓
Google Gemini AI Generates Answer
        ↓
System Shows Answer + Source Documents
```

---

## Troubleshooting in 30 Seconds

### "Port 8000 is already in use"
Use a different port:
```bash
python -m uvicorn backend.main:app --port 8001
```

### "ModuleNotFoundError"
Install dependencies:
```bash
pip install -r requirements.txt
```

### "GEMINI_API_KEY is not set"
1. Get key: https://makersuite.google.com/app/apikey
2. Edit `.env` file
3. Add: `GEMINI_API_KEY=your_key_here`

### Still stuck?
See detailed troubleshooting: [HOW_TO_RUN.md#troubleshooting](./HOW_TO_RUN.md#troubleshooting)

---

## Three Ways to Use It

### Way 1: Web Interface (Easiest)
- Open http://localhost:8501
- Type questions
- Upload documents
- No technical knowledge needed

### Way 2: REST API (For Developers)
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me something"}'
```

### Way 3: Python Scripts
```bash
python -m scripts.ingest_documents --mode sample
```

---

## Key Features You'll Love

✅ **No Database Setup** - Works out of the box

✅ **Supports Multiple Formats** - PDF, TXT, Markdown

✅ **Remembers Conversations** - Context-aware responses

✅ **Shows Sources** - See which documents answered you

✅ **Fast & Accurate** - AI-powered semantic search

✅ **Free to Use** - Only need a free Gemini API key

✅ **Scalable** - Works with 10 or 10,000 documents

---

## System Requirements Check

Run this to verify everything:

```bash
# Check Python version
python --version  # Should be 3.9 or higher

# Check pip
pip --version

# Check internet connection
curl http://api.openai.com  # Just testing connectivity
```

All good? You're ready to start!

---

## File Guide

If you want to explore:

| File | Purpose |
|------|---------|
| `start.sh` | One-command startup script |
| `.env.example` | Configuration template |
| `requirements.txt` | Python dependencies list |
| `backend/main.py` | REST API server |
| `frontend/streamlit_app.py` | Web interface |
| `backend/rag_pipeline.py` | AI processing logic |

---

## What Happens When You Start

1. **Backend Server Starts** (port 8000)
   - REST API ready
   - AI models loaded
   - Connected to Gemini API

2. **Frontend Server Starts** (port 8501)
   - Web interface ready
   - Chat system active
   - Document upload enabled

3. **In-Memory Storage Ready**
   - Embeddings stored in memory
   - No database installation needed
   - Data lost when you restart (unless using Endee)

---

## Next Steps

1. **Right now:** Follow one of the three paths above
2. **After it works:** Upload your own documents
3. **Want more:** Read [AI_KNOWLEDGE_ASSISTANT_README.md](./AI_KNOWLEDGE_ASSISTANT_README.md)
4. **Need customization:** See [DEVELOPMENT.md](./DEVELOPMENT.md)

---

## Documentation Map

```
START_HERE.md (you are here!)
    ↓
    Choose one:
    ├─ HOW_TO_RUN.md (detailed guide)
    ├─ QUICKSTART.md (fast path)
    └─ README_AI_ASSISTANT.md (overview)
    ↓
    Advanced topics:
    ├─ DEVELOPMENT.md (architecture)
    ├─ AI_KNOWLEDGE_ASSISTANT_README.md (features)
    └─ PROJECT_STRUCTURE.md (file layout)
```

---

## Common Questions

**Q: Do I need to install Endee?**
A: No! The system works without it. Endee is optional for production use.

**Q: Is the Gemini API key free?**
A: Yes! Get a free tier key at https://makersuite.google.com/app/apikey

**Q: Can I upload my own documents?**
A: Yes! Supports PDF, TXT, and Markdown files.

**Q: How many documents can it handle?**
A: Thousands! Performance depends on your system resources.

**Q: Is my data private?**
A: Yes! Everything runs locally or on your servers.

**Q: Can I use a different AI model?**
A: Yes! See [DEVELOPMENT.md](./DEVELOPMENT.md) for configuration options.

---

## Your Next Command

Pick one and run it:

**Option A - Fastest:**
```bash
chmod +x start.sh && ./start.sh
```

**Option B - Docker:**
```bash
docker-compose -f docker-compose-app.yml up
```

**Option C - Manual:**
```bash
source venv/bin/activate
python -m uvicorn backend.main:app --reload
```

Then open: http://localhost:8501

---

## You're Ready!

That's all you need to know to get started. The system will guide you from there.

### Three simple steps:
1. Start the application
2. Upload a document
3. Ask a question

Questions? Check [HOW_TO_RUN.md](./HOW_TO_RUN.md#troubleshooting)

---

**Let's go! 🚀**

Run `./start.sh` now and see your AI assistant in action!
