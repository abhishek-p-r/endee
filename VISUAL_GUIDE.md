# Visual Guide - How to Run Endee AI Assistant

A quick visual reference for getting started and using the system.

---

## Step 1: Before You Start

```
┌─────────────────────────────────────────┐
│ What You Need:                          │
├─────────────────────────────────────────┤
│ ✅ Python 3.9+ (or Docker)              │
│ ✅ Gemini API Key (FREE)                │
│ ✅ Internet connection                  │
│ ✅ 4 GB RAM minimum                     │
│ ✅ 2 GB disk space                      │
└─────────────────────────────────────────┘

Get your FREE Gemini API Key:
→ Visit: https://makersuite.google.com/app/apikey
→ Click: "Create API Key"
→ Copy: the key that appears
→ Keep it safe!
```

---

## Step 2: Choose Your Setup Method

```
                    START HERE
                        ↓
    ┌───────────────────┼───────────────────┐
    ↓                   ↓                   ↓
EASIEST            DETAILED            DOCKER
(5 min)            (10-15 min)         (10 min)

./start.sh      Follow HOW_TO_RUN.md   docker-compose
    ↓                   ↓                   ↓
   Run                 Run                 Run
   Script             Manual              Container
    ↓                   ↓                   ↓
  All Done!         All Done!           All Done!
```

---

## Method A: Automated Script (Easiest)

```bash
┌────────────────────────────────────────┐
│ TERMINAL:                              │
├────────────────────────────────────────┤
│ $ cd endee-ai-knowledge-assistant      │
│ $ chmod +x start.sh                    │
│ $ ./start.sh                           │
│                                        │
│ [Waiting...]                           │
│                                        │
│ Enter Gemini API Key:                  │
│ [Paste your key here]                  │
│                                        │
│ ✅ Backend started (port 8000)         │
│ ✅ Frontend started (port 8501)        │
│                                        │
│ Opening browser...                     │
└────────────────────────────────────────┘
```

---

## Method B: Step-by-Step (Detailed)

```
Step 1: Create Environment
┌─────────────────────────────────┐
│ python -m venv venv             │
│ source venv/bin/activate        │
│ (or: venv\Scripts\activate)    │
└─────────────────────────────────┘
        ↓
Step 2: Install Dependencies
┌─────────────────────────────────┐
│ pip install -r requirements.txt │
│ (takes 2-3 minutes)             │
└─────────────────────────────────┘
        ↓
Step 3: Configure
┌─────────────────────────────────┐
│ cp .env.example .env            │
│ nano .env                       │
│ Add: GEMINI_API_KEY=your_key   │
└─────────────────────────────────┘
        ↓
Step 4: Start (Terminal 1)
┌─────────────────────────────────┐
│ source venv/bin/activate        │
│ python -m uvicorn backend.main:app --reload  │
└─────────────────────────────────┘
        ↓
Step 5: Start (Terminal 2)
┌─────────────────────────────────┐
│ source venv/bin/activate        │
│ streamlit run frontend/streamlit_app.py      │
└─────────────────────────────────┘
        ↓
       Done!
```

---

## Method C: Docker (Modern)

```bash
┌────────────────────────────────────────┐
│ TERMINAL:                              │
├────────────────────────────────────────┤
│ $ docker-compose -f docker-compose-app.yml up │
│                                        │
│ [Docker building images...]            │
│ [Docker starting services...]          │
│                                        │
│ ✅ Backend ready                       │
│ ✅ Frontend ready                      │
│                                        │
│ Open browser →                         │
│ http://localhost:8501                  │
│                                        │
│ (No setup needed!)                    │
└────────────────────────────────────────┘
```

---

## What's Running After Startup

```
Your Computer
├─ FastAPI Backend
│  ├─ Port: 8000
│  ├─ URL: http://localhost:8000
│  └─ API Docs: http://localhost:8000/docs
│
├─ Streamlit Frontend
│  ├─ Port: 8501
│  ├─ URL: http://localhost:8501
│  └─ Main chat interface
│
└─ Storage
   └─ In-memory vectors (no database needed!)
```

---

## Access Points After Startup

```
┌────────────────────────────────────────────┐
│ Web Browser - Visit These URLs:            │
├────────────────────────────────────────────┤
│                                            │
│ 🎯 http://localhost:8501                   │
│    └─ MAIN APP - Use this!                 │
│       • Chat interface                     │
│       • Document upload                    │
│       • View answers                       │
│                                            │
│ 📚 http://localhost:8000/docs              │
│    └─ API Documentation                    │
│       • Test endpoints                     │
│       • See parameters                     │
│       • Try requests                       │
│                                            │
│ 📖 http://localhost:8000/redoc             │
│    └─ Alternative API Docs                 │
│                                            │
└────────────────────────────────────────────┘
```

---

## First Use: Step-by-Step

```
┌──────────────────────────────────┐
│ STEP 1: Open Web Interface       │
├──────────────────────────────────┤
│ Browser: http://localhost:8501   │
│          ↓                       │
│          (You see chat window)   │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ STEP 2: Upload a Document        │
├──────────────────────────────────┤
│ Click: "📚 Document Upload"      │
│ Choose: Your PDF/TXT file        │
│ Click: "📤 Upload & Ingest"      │
│ Wait: "✅ Success" message       │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ STEP 3: Ask a Question           │
├──────────────────────────────────┤
│ Type: "What did I upload?"       │
│ Press: Enter                     │
│ Wait: 5-10 seconds               │
│ See: Answer with sources         │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ STEP 4: View More Details        │
├──────────────────────────────────┤
│ Click: "📊 Response Details"     │
│ See: Which documents were used   │
│ See: Query analysis              │
│ See: Key points                  │
└──────────────────────────────────┘

✅ YOU'RE DONE!
   Keep asking questions and uploading files
```

---

## How the System Works (Visual)

```
┌────────────┐
│   You Ask  │ "What is in my document?"
└─────┬──────┘
      ↓
┌─────────────────────────────────────────┐
│ SYSTEM PROCESSES YOUR QUESTION           │
├─────────────────────────────────────────┤
│                                         │
│ 1. Query Bot                            │
│    └─ Makes your question better        │
│    └─ Understands what you mean         │
│       ↓                                 │
│                                         │
│ 2. Retrieval Bot                        │
│    └─ Searches your documents           │
│    └─ Finds similar content             │
│       ↓                                 │
│                                         │
│ 3. Reasoning Bot (Gemini AI)            │
│    └─ Reads found content               │
│    └─ Thinks about your question        │
│    └─ Writes the answer                 │
│       ↓                                 │
│                                         │
│ 4. Formatting Bot                       │
│    └─ Makes answer readable             │
│    └─ Adds sources                      │
│    └─ Prepares for display              │
│       ↓                                 │
└─────┬───────────────────────────────────┘
      ↓
┌──────────────────┐
│ Answer appears   │ "Your document is about..."
│ With sources     │ [Source: document.pdf]
└──────────────────┘
```

---

## File Structure (Simplified)

```
endee-ai-knowledge-assistant/
│
├─ 🚀 START HERE FILES
│  ├─ START_HERE.md ..................... Quick intro
│  ├─ HOW_TO_RUN.md .................... Setup guide
│  ├─ QUICKSTART.md .................... Fast setup
│  └─ start.sh ......................... Run script
│
├─ 📱 FRONTEND (Web Interface)
│  └─ frontend/
│     └─ streamlit_app.py .............. Chat app
│
├─ ⚙️  BACKEND (API)
│  └─ backend/
│     ├─ main.py ....................... REST API
│     ├─ rag_pipeline.py ............... AI logic
│     ├─ bots/ ......................... AI agents
│     │  ├─ query_bot.py
│     │  ├─ retrieval_bot.py
│     │  ├─ reasoning_bot.py
│     │  └─ formatter_bot.py
│     ├─ embeddings.py ................. Vectors
│     ├─ gemini_client.py .............. Gemini API
│     └─ config.py ..................... Settings
│
├─ 🧪 SCRIPTS (Utilities)
│  └─ scripts/
│     ├─ ingest_documents.py ........... Upload docs
│     └─ test_api.py ................... Test API
│
├─ 📖 DOCUMENTATION
│  ├─ README_AI_ASSISTANT.md
│  ├─ AI_KNOWLEDGE_ASSISTANT_README.md
│  ├─ DEVELOPMENT.md
│  ├─ DOCUMENTATION_INDEX.md
│  └─ (more detailed docs)
│
├─ 🐳 DEPLOYMENT
│  ├─ Dockerfile
│  ├─ docker-compose-app.yml
│  └─ requirements.txt
│
└─ ⚙️  CONFIGURATION
   ├─ .env.example ..................... Settings
   └─ .env ............................ Your settings
```

---

## Common Tasks - Quick Reference

```
TASK: Upload a Document
┌─────────────────────────────────────────┐
│ 1. Open: http://localhost:8501          │
│ 2. Click: "📚 Document Upload"          │
│ 3. Select: Your file (PDF/TXT/MD)       │
│ 4. Click: "📤 Upload & Ingest"          │
│ 5. Wait: "✅ Success"                   │
└─────────────────────────────────────────┘

TASK: Ask a Question
┌─────────────────────────────────────────┐
│ 1. Type in chat box                     │
│ 2. Press Enter                          │
│ 3. Wait 5-10 seconds                    │
│ 4. Read answer + sources                │
└─────────────────────────────────────────┘

TASK: View Response Details
┌─────────────────────────────────────────┐
│ 1. Look for message in chat             │
│ 2. Click: "📊 Response Details"         │
│ 3. See: Sources and analysis            │
└─────────────────────────────────────────┘

TASK: Access API
┌─────────────────────────────────────────┐
│ 1. Visit: http://localhost:8000/docs    │
│ 2. Find endpoint                        │
│ 3. Click "Try it out"                   │
│ 4. Enter parameters                     │
│ 5. Click "Execute"                      │
└─────────────────────────────────────────┘

TASK: Ingest Sample Documents
┌─────────────────────────────────────────┐
│ $ python -m scripts.ingest_documents \  │
│   --mode sample                         │
└─────────────────────────────────────────┘

TASK: Stop the Application
┌─────────────────────────────────────────┐
│ In Terminal: Press Ctrl + C             │
│ Or: docker-compose down (if Docker)     │
└─────────────────────────────────────────┘
```

---

## Troubleshooting - Quick Fixes

```
PROBLEM: Won't start
┌─────────────────────────────────────────┐
│ Check: Port 8000 in use                 │
│ Fix: Use different port or kill process │
└─────────────────────────────────────────┘

PROBLEM: API Key error
┌─────────────────────────────────────────┐
│ Check: https://makersuite.google.com    │
│ Fix: Add key to .env file               │
│ Restart: Application                    │
└─────────────────────────────────────────┘

PROBLEM: Module not found
┌─────────────────────────────────────────┐
│ Fix: pip install -r requirements.txt    │
│ Check: Virtual environment activated    │
└─────────────────────────────────────────┘

PROBLEM: Slow response
┌─────────────────────────────────────────┐
│ Note: First request loads models (slow) │
│ Subsequent requests are faster          │
│ Check: System resources (RAM/CPU)       │
└─────────────────────────────────────────┘

→ More help: See HOW_TO_RUN.md
```

---

## URL Quick Reference

```
┌────────────────────────────────────────────────┐
│ WHAT YOU USE                   URL             │
├────────────────────────────────────────────────┤
│ Main Chat Interface           localhost:8501   │
│ API Documentation             localhost:8000   │
│ API Testing                   localhost:8000/docs │
│ Health Check                  localhost:8000/health │
├────────────────────────────────────────────────┤
│ GET Gemini API Key            makersuite.      │
│                               google.com/app   │
│                               /apikey          │
│ Endee Database                github.com/      │
│ (Optional)                    endee-io/endee  │
└────────────────────────────────────────────────┘
```

---

## Setup Time Comparison

```
┌─────────────────────────────────────────┐
│ METHOD          TIME      DIFFICULTY    │
├─────────────────────────────────────────┤
│ Script          5 min     ⭐ Very Easy  │
│ Step-by-Step    15 min    ⭐⭐ Easy    │
│ Docker          10 min    ⭐⭐ Easy    │
│ Manual Setup    20 min    ⭐⭐⭐ Medium│
└─────────────────────────────────────────┘

👉 RECOMMENDATION: Use Script (./start.sh)
```

---

## System Architecture (Simplified)

```
                     USERS
                      ↓
              ┌───────────────┐
              │  Browser (UI) │ port 8501
              └───────┬───────┘
                      ↓
            ┌─────────────────────┐
            │ Streamlit Frontend  │
            │  (Chat Interface)   │
            └──────────┬──────────┘
                       ↓
        ┌──────────────────────────────┐
        │     FastAPI Backend          │ port 8000
        │    (REST API Server)         │
        └──────────┬───────────────────┘
                   ↓
      ┌────────────┴────────────┐
      ↓                         ↓
  ┌────────────┐         ┌──────────────┐
  │ RAG Engine │         │   Gemini AI  │
  │ (Endee or  │         │   (LLM)      │
  │  In-Memory)│         │              │
  └────────────┘         └──────────────┘
      ↓
  ┌────────────────┐
  │ Your Documents │
  │ (Embeddings)   │
  └────────────────┘
```

---

## Next Actions

Choose your path:

```
┌─────────────────────────────────────────┐
│ ALREADY FAMILIAR WITH PYTHON?           │
│ → Run: ./start.sh                       │
│ → Read: QUICKSTART.md                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ NEW TO THIS KIND OF SYSTEM?             │
│ → Start: START_HERE.md                  │
│ → Follow: HOW_TO_RUN.md                 │
│ → Then: Open http://localhost:8501      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ WANT TO CUSTOMIZE OR DEVELOP?           │
│ → Setup: HOW_TO_RUN.md                  │
│ → Learn: DEVELOPMENT.md                 │
│ → Code: backend/ and frontend/          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ DEPLOYING TO PRODUCTION?                │
│ → Setup: HOW_TO_RUN.md                  │
│ → Deploy: Use docker-compose            │
│ → Configure: DEVELOPMENT.md             │
└─────────────────────────────────────────┘
```

---

## Remember

```
     You are only 3 steps away from success:
     
     1️⃣  Get Gemini API Key
         (https://makersuite.google.com/app/apikey)
     
     2️⃣  Run ./start.sh
     
     3️⃣  Open http://localhost:8501
     
     That's it! 🎉
```

---

**You've got this! Let's go build something amazing!** 🚀

For more details, see [START_HERE.md](./START_HERE.md)
