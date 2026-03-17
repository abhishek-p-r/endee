# Troubleshooting Guide

## Common Issues & Solutions

### Connection Issues

#### "Cannot connect to Endee at localhost:8001"

**Cause**: Endee service not running

**Solutions**:
```bash
# Check if Endee is running
curl http://localhost:8001/health

# Start with Docker
docker run -d -p 8001:8001 endeeio/endee:latest

# Or with Docker Compose
docker-compose up endee-db -d

# Check logs
docker logs endee-db
```

#### "Connection refused on port 8000"

**Cause**: Backend not running or port in use

**Solutions**:
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Start backend
python -m uvicorn backend.app:app --port 8000
```

### OpenAI Issues

#### "Invalid OpenAI API key"

**Cause**: Missing or incorrect API key

**Solutions**:
```bash
# Verify key is set
echo $OPENAI_API_KEY
# Should start with 'sk-'

# If not set:
export OPENAI_API_KEY=sk-your-actual-key

# Or add to .env file
nano .env
# OPENAI_API_KEY=sk-...

# Restart backend service
```

#### "Insufficient quota on OpenAI account"

**Cause**: Free credits expired or billing issue

**Solutions**:
1. Check quota at https://platform.openai.com/account/billing/overview
2. Add payment method
3. Check usage limits
4. Consider cheaper models (gpt-3.5-turbo)

#### "OpenAI API rate limited"

**Cause**: Too many requests too quickly

**Solutions**:
```bash
# Wait a few seconds and retry
# Or implement exponential backoff in your code

# Check rate limits
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Document Upload Issues

#### "File too large"

**Cause**: Document exceeds size limits

**Solutions**:
```bash
# Split large PDF
# Recommended max: 50MB

# Or adjust in backend/config.py
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

#### "Unsupported file format"

**Cause**: File is not PDF, TXT, or Markdown

**Solutions**:
```bash
# Supported formats:
# - .pdf (PDF documents)
# - .txt (Plain text)
# - .md  (Markdown)

# Convert other formats:
# Word -> PDF (use LibreOffice)
# HTML -> Markdown (use Pandoc)
```

#### "No text extracted from PDF"

**Cause**: PDF is scanned image, not text

**Solutions**:
```bash
# Use OCR on PDF
# Option 1: Online tool like ILovePDF
# Option 2: Local tool like OCRmyPDF
ocrmypdf input.pdf output.pdf

# Then upload output.pdf
```

### Search & Query Issues

#### "No results found"

**Cause**: Documents not uploaded or irrelevant query

**Solutions**:
```bash
# Verify documents uploaded
curl http://localhost:8000/api/documents/list

# Upload documents
# Use web UI or API to upload

# Try different search terms
# Be more specific (e.g., "Python installation steps" instead of "help")

# Increase top_k in settings
# From 5 to 10 or 15
```

#### "Slow query responses"

**Cause**: System overloaded or network delay

**Solutions**:
```bash
# Check cache hit rate
curl http://localhost:8000/api/cache/stats

# Clear cache if needed
curl -X POST http://localhost:8000/api/cache/clear

# Reduce document size or chunk size
# In backend/config.py
CHUNK_SIZE = 500  # Reduce from 1000

# Restart services
docker-compose restart
```

#### "Low quality answers"

**Cause**: Poor document retrieval or LLM model limitations

**Solutions**:
```bash
# Check retrieved sources
# Use /api/search to see what's found

# Improve document quality
# Add more context, better formatting

# Use better LLM model
# In backend/config.py
OPENAI_LLM_MODEL = "gpt-4"  # More powerful

# Adjust search parameters
# Increase top_k, lower threshold
```

### Memory & Performance Issues

#### "Out of memory (OOM)"

**Cause**: Processing large documents

**Solutions**:
```bash
# Reduce chunk size
# In backend/config.py
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Process smaller files
# Split large documents first

# Increase system RAM
# Allocate more to Docker
docker update --memory 8g <container_id>

# Increase swap
# On Linux: sudo fallocate -l 4G /swapfile
```

#### "Slow embeddings generation"

**Cause**: Using CPU for embeddings

**Solutions**:
```bash
# Use GPU if available
# Requires CUDA setup

# Or use faster embedding model
# In backend/config.py
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# Batch multiple documents
# Upload several at once
```

### Docker Issues

#### "Docker container won't start"

**Cause**: Port conflict or configuration error

**Solutions**:
```bash
# Check logs
docker-compose logs backend

# Check if ports are in use
lsof -i :8000
lsof -i :8501
lsof -i :8001

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check disk space
df -h
```

#### "docker-compose command not found"

**Cause**: Docker Compose not installed

**Solutions**:
```bash
# Install Docker Desktop (includes Compose)
# Or install standalone:

# macOS
brew install docker-compose

# Linux
sudo curl -L \
  "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Web UI Issues

#### "Streamlit not loading"

**Cause**: Frontend service not running

**Solutions**:
```bash
# Check if running
curl http://localhost:8501

# Restart frontend
docker-compose restart frontend

# Or manual start
streamlit run frontend/app.py --server.port 8501
```

#### "UI updates not reflecting"

**Cause**: Browser cache

**Solutions**:
```bash
# Clear browser cache
# Ctrl+Shift+Delete (Windows)
# Cmd+Shift+Delete (Mac)

# Or disable cache in browser dev tools
# F12 -> Network tab -> Disable cache
```

### Network Issues

#### "Cross-Origin Request Blocked"

**Cause**: CORS policy for different domains

**Solutions**:
```python
# In backend/app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### "Request timeout"

**Cause**: Network too slow or request too large

**Solutions**:
```python
# Increase timeout in client
# Default: 30 seconds

import requests
requests.post(
    url,
    json=data,
    timeout=60  # 60 seconds
)
```

## Debugging Tips

### Enable Debug Logging

```bash
# In .env
LOG_LEVEL=DEBUG

# Restart backend
docker-compose restart backend
```

### Check Service Logs

```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Endee logs
docker-compose logs -f endee-db
```

### Run System Verification

```bash
python scripts/verify_setup.py

# Detailed check
python scripts/verify_setup.py --verbose
```

### Test API Directly

```bash
# Health check all services
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8501

# Test specific endpoint
curl -X POST http://localhost:8000/api/query/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test question"}'
```

## Getting Help

1. **Check this guide** - Most issues covered here
2. **Run verification** - `python scripts/verify_setup.py`
3. **Check logs** - `docker-compose logs`
4. **Restart services** - `docker-compose restart`
5. **GitHub Issues** - Open an issue on GitHub

## Advanced Debugging

### Profile System Performance

```bash
# Monitor resource usage
docker stats

# Top consuming containers
docker ps --format \
  "{{.Names}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Debug API Requests

```bash
# Capture all HTTP requests
# In terminal before starting backend:
export PYTHONUNBUFFERED=1

# Start backend with detailed output
python -m uvicorn backend.app:app --log-level debug
```

### Test with Different Models

```python
# In backend/config.py
# Try cheaper/faster models for debugging
OPENAI_LLM_MODEL = "gpt-3.5-turbo"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
```

## Performance Optimization

See [README.md#performance](../README.md#performance) for detailed optimization tips.
