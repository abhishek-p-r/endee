# 🚀 Quick Reference Guide

## 📍 Where to Start?

```
🤔 "I want to..."
    ├─ Get it running NOW → QUICKSTART.md
    ├─ Understand what this is → README_PROJECT.md
    ├─ Find a specific file → PROJECT_STRUCTURE.md
    ├─ Modify the code → DEVELOPMENT.md
    ├─ See everything that was built → COMPLETION_CHECKLIST.md
    └─ Choose my path → GETTING_STARTED.md
```

## ⚡ Super Quick Commands

### Start Everything
```bash
chmod +x start.sh && ./start.sh
```

### Start Backend Only
```bash
python -m uvicorn backend.main:app --reload
```

### Start Frontend Only
```bash
streamlit run frontend/streamlit_app.py
```

### Ingest Sample Documents
```bash
python -m scripts.ingest_documents --mode sample
```

### Test the API
```bash
python -m scripts.test_api
```

### With Docker
```bash
docker-compose -f docker-compose-app.yml up
```

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Web UI** | http://localhost:8501 | Chat & Documents |
| **API Docs** | http://localhost:8000/docs | Interactive API |
| **ReDoc** | http://localhost:8000/redoc | Alternative API Docs |
| **Health Check** | http://localhost:8000/health | Server Status |
| **Endee DB** | http://localhost:8080 | Vector Database |

## 🔧 Configuration

### Must Configure
```env
GEMINI_API_KEY=your_api_key_here
```

### Optional (Defaults Provided)
```env
ENDEE_URL=http://localhost:8080
SERVER_PORT=8000
DEBUG=False
```

### Get Gemini Key
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `.env`

## 📝 File Types Supported

✅ **PDF** - Automatic text extraction
✅ **TXT** - Plain text
✅ **MD** - Markdown files

Upload via web UI or command line:
```bash
python -m scripts.ingest_documents --mode file --path document.pdf
```

## 🤖 The 4 Bots Explained

### 1️⃣ Query Bot
```
Input: "What is machine learning?"
↓
Output: {
  "intent": "definition",
  "optimized": "machine learning definition explanation",
  "keywords": ["machine", "learning", "definition"]
}
```

### 2️⃣ Retrieval Bot
```
Input: Optimized query + embeddings
↓
Output: Top 5 relevant documents from Endee
```

### 3️⃣ Reasoning Bot
```
Input: Question + retrieved context
↓
Output: "Machine learning is a subset of AI that..."
```

### 4️⃣ Formatter Bot
```
Input: Raw answer
↓
Output: {
  "answer": "...",
  "key_points": [...],
  "sources": [...]
}
```

## 🔌 API Quick Reference

### Ask a Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "session_id": "user_1"
  }'
```

### Upload a Document
```bash
curl -X POST http://localhost:8000/ingest/upload \
  -F "file=@document.pdf" \
  -F "source=My Document"
```

### Check Health
```bash
curl http://localhost:8000/health
```

### Get Chat History
```bash
curl http://localhost:8000/chat/history/user_1
```

### Clear Chat History
```bash
curl -X DELETE http://localhost:8000/chat/history/user_1
```

## 🎯 Common Workflows

### Workflow 1: Basic Setup
```
1. cp .env.example .env
2. Add GEMINI_API_KEY to .env
3. ./start.sh
4. Open http://localhost:8501
```

### Workflow 2: Upload & Ask
```
1. Click "📚 Document Upload" in sidebar
2. Upload a PDF/TXT/MD file
3. Click "📤 Upload & Ingest"
4. Wait for confirmation
5. Ask a question about it
```

### Workflow 3: Batch Ingest
```
1. Put documents in a directory
2. Run: python -m scripts.ingest_documents --mode directory --path ./documents
3. Check results
4. Start asking questions
```

### Workflow 4: API Integration
```
1. Start backend: python -m uvicorn backend.main:app
2. Make POST request to /ask endpoint
3. Process response JSON
4. Display to user
```

## 🧪 Testing Checklist

Before going live, verify:

```
□ Backend starts without errors
  curl http://localhost:8000/health

□ Frontend loads
  Open http://localhost:8501

□ Can ingest documents
  python -m scripts.ingest_documents --mode sample

□ Can ask questions
  Type in chat interface

□ Can view sources
  Click "Response Details"

□ Can manage sessions
  Change session ID, ask questions

□ API works
  Use scripts/test_api.py
```

## 📊 Performance Tips

### For Large Document Sets
- Use batch ingestion: `--mode directory`
- Increase chunk_size in config for longer docs
- Reduce max_retrieved_documents if too slow

### For Fast Responses
- Reduce chunk_size (smaller = faster search)
- Use fewer max_retrieved_documents
- Increase similarity_threshold

### Memory Usage
- Conversation history limited to 10 messages
- Clear old sessions regularly
- Monitor logs for memory issues

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | `lsof -i :8000` then kill process |
| Gemini API error | Check API key in .env |
| Endee not found | Optional - start separately or ignore |
| Port already in use | Use different port: `--port 8001` |
| Slow search | Reduce max_retrieved_documents |
| Memory issues | Clear chat history: DELETE endpoint |

## 📚 Documentation Hierarchy

```
START HERE ↓

README_PROJECT.md
(Overview of everything)
       ↓
Choose your path:
├─ QUICKSTART.md (Fast setup)
├─ GETTING_STARTED.md (Choose your way)
├─ AI_KNOWLEDGE_ASSISTANT_README.md (Full details)
├─ DEVELOPMENT.md (Customize)
└─ PROJECT_STRUCTURE.md (Find files)

For details on specific file:
└─ PROJECT_STRUCTURE.md → Find file → Edit
```

## 🎯 Success Indicators

You'll know it's working when:
- ✅ Backend returns 200 on /health
- ✅ Frontend loads without errors
- ✅ Can ask a question
- ✅ Get back an answer
- ✅ See sources displayed
- ✅ Can upload documents
- ✅ Can view chat history

## 🚀 Next Steps

### Immediate
1. Get it running: `./start.sh`
2. Try the UI: http://localhost:8501
3. Ask a test question
4. Upload a document

### Short Term (Day 1)
1. Read QUICKSTART.md fully
2. Understand the architecture
3. Test all features
4. Check the logs

### Medium Term (Week 1)
1. Read DEVELOPMENT.md
2. Customize prompts
3. Adjust parameters
4. Deploy to your server

### Long Term (Production)
1. Add authentication
2. Set up monitoring
3. Configure backups
4. Load test
5. Security audit

## 💡 Pro Tips

### Tip 1: Custom Prompts
Edit bot files in `backend/bots/` to change how AI behaves:
```python
prompt = f"Your custom prompt here: {question}"
```

### Tip 2: Different Embedding Models
Edit `backend/config.py`:
```python
embedding_model: str = "all-mpnet-base-v2"  # Different model
```

### Tip 3: Fast Testing
Use test script to verify everything:
```bash
python -m scripts.test_api --test flow
```

### Tip 4: Check Logs
Real-time debugging:
```bash
tail -f logs/app_*.log
```

### Tip 5: API First Development
Build backend first, add UI later:
```bash
python -m uvicorn backend.main:app --reload
# Then test with curl or Postman
```

## 🔐 Security Reminders

- Never commit `.env` file
- Keep API key private
- Use HTTPS in production
- Add authentication for multi-user
- Implement rate limiting
- Monitor logs for issues
- Update dependencies regularly

## 📞 Getting Help

| Issue | Resource |
|-------|----------|
| Setup problems | QUICKSTART.md → Troubleshooting |
| Understanding system | README_PROJECT.md |
| Code questions | DEVELOPMENT.md |
| File location | PROJECT_STRUCTURE.md |
| API docs | http://localhost:8000/docs |
| Endee issues | https://github.com/endee-io/endee |
| Gemini API | https://ai.google.dev/ |

## 🎉 You're Ready!

```
🎯 Goal: Get it running ✅
├─ ./start.sh ...................... 3 minutes
├─ Open http://localhost:8501 ....... 10 seconds
├─ Upload a document ............... 30 seconds
├─ Ask a question .................. 15 seconds
└─ See the answer with sources ...... ✨ Magic

Total time to first working system: ~5 minutes
```

---

**Last Updated**: March 2026

**Quick Links**:
- 🚀 [QUICKSTART.md](QUICKSTART.md) - Start here
- 📖 [README_PROJECT.md](README_PROJECT.md) - Full overview
- 👨‍💻 [DEVELOPMENT.md](DEVELOPMENT.md) - Customize
- 🗂️ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Find files

**Status**: ✅ Ready to use right now!
