# Quick Start Guide - 5 Minutes to RAG

## The Fastest Way to Get Started

### Step 1: Get OpenAI API Key (1 minute)

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

### Step 2: Clone & Configure (2 minutes)

```bash
# Clone
git clone https://github.com/abhishek-p-r/endee.git
cd endee

# Configure
cp .env.example .env
# Edit .env and add your OpenAI key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Start Everything (2 minutes)

```bash
docker-compose up -d

# Wait 30 seconds for services to start
sleep 30

# Open browser
open http://localhost:8501
```

### Done! Now What?

1. **Upload Documents** - Click "Upload Documents" tab, select PDF/TXT/MD files
2. **Ask Questions** - Click "Chat" tab, type your question
3. **Get Answers** - See AI response with source documents
4. **Explore** - Try search, analytics, and settings tabs

### Troubleshooting Quick Fixes

**Port in use?**
```bash
# Kill the process
lsof -i :8501 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

**API key invalid?**
```bash
# Verify key format
echo $OPENAI_API_KEY  # Should start with sk-
# Get new key: https://platform.openai.com/api-keys
```

**Services not starting?**
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend
```

**Want to stop?**
```bash
docker-compose down
```

---

## Detailed Installation (If Docker Doesn't Work)

### Manual Setup (3 Terminals)

**Terminal 1: Start Endee**
```bash
docker run -p 8001:8001 endeeio/endee:latest
```

**Terminal 2: Start Backend**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn backend.app:app --port 8000 --reload
```

**Terminal 3: Start Frontend**
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
streamlit run frontend/app.py --server.port 8501
```

---

## First Test: Upload a Document & Ask a Question

1. Create a test file `test.txt`:
```
Machine learning is a subset of artificial intelligence that focuses on 
the development of algorithms and models that can learn from and make 
predictions on data. It's used in recommendation systems, image recognition, 
natural language processing, and many other applications.
```

2. Open http://localhost:8501
3. Click "Upload Documents" → Select `test.txt` → Click "Process"
4. Click "Chat" → Type: "What is machine learning?"
5. Click Send → Get instant AI answer!

---

## Verify Everything Works

```bash
# Test API health
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# Test Endee
curl http://localhost:8001/health
# Should return: {"status": "healthy"}

# Run verification script
python scripts/verify_setup.py
# Should show all checks passing
```

---

## Next Steps

- Read full [README.md](README.md) for advanced features
- Check [docs/](docs/) for detailed guides
- View API docs at http://localhost:8000/docs
- Run demo: `python scripts/demo.py`

---

## Common Questions

**Q: How much does this cost?**  
A: Only OpenAI API usage (embeddings: ~$0.02/1M tokens, LLM: ~$0.15/1M input tokens)

**Q: How many documents can I store?**  
A: Unlimited - limited only by disk space

**Q: Can I use different LLMs?**  
A: Yes! Change `OPENAI_LLM_MODEL` in `.env`

**Q: Is my data secure?**  
A: Your data stays on your server (self-hosted option available)

**Q: Can I deploy to production?**  
A: Yes! See README.md deployment section

---

**Having issues? Check [README.md#troubleshooting](README.md#troubleshooting) for detailed solutions.**
