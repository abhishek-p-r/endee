# Verification Checklist - Endee AI Knowledge Assistant

**Purpose**: Confirm all systems are working correctly after setup

**Total Checks**: 30
**Expected Time**: 10 minutes

---

## Pre-Setup Verification

### Check 1: Environment ✓
```bash
python --version
# Expected: Python 3.8 or higher
```

### Check 2: Git
```bash
git --version
# Expected: git version 2.x+
```

### Check 3: Repository
```bash
cd endee
git status
# Expected: On branch endee-ai-assistant
```

### Check 4: Files Exist
```bash
ls -la | grep -E "requirements.txt|.env.example|README.md"
# Expected: All files present
```

---

## Installation Verification

### Check 5: Virtual Environment ✓
```bash
source venv/bin/activate
python -c "import sys; print(sys.prefix)"
# Expected: Path ending in /venv
```

### Check 6: Dependencies Installed ✓
```bash
pip list | grep -E "fastapi|streamlit|sentence-transformers|google-generativeai"
# Expected: All packages listed
```

### Check 7: Environment File ✓
```bash
ls -la .env
# Expected: .env file exists
cat .env | head -5
# Expected: Shows configuration
```

### Check 8: API Key Set ✓
```bash
grep GEMINI_API_KEY .env
# Expected: GEMINI_API_KEY=sk_...
```

---

## Endee Database Verification

### Check 9: Endee Running ✓
```bash
curl http://localhost:8080/health
# Expected: {"status": "healthy"} or similar healthy response
```

### Check 10: Endee Version ✓
```bash
curl http://localhost:8080/version 2>/dev/null || echo "Status check only"
# Expected: Version info or confirmation
```

### Check 11: Collection Access ✓
```bash
curl http://localhost:8080/collections 2>/dev/null
# Expected: Collection list or empty list
```

---

## Document Processing Verification

### Check 12: Data Directory ✓
```bash
ls -la data/
# Expected: .txt files present or "No such file or directory" (will create)
```

### Check 13: Ingestion Script ✓
```bash
python scripts/ingest_documents.py --help
# Expected: Shows script help/usage
```

### Check 14: Run Ingestion ✓
```bash
python scripts/ingest_documents.py
# Expected: Successfully ingests documents and stores vectors
```

### Check 15: Verify Ingestion ✓
```bash
curl http://localhost:8080/collections 2>/dev/null | grep -i knowledge_base
# Expected: Shows knowledge_base collection
```

---

## Backend API Verification

### Check 16: API Server ✓
```bash
python -m uvicorn backend.main:app --reload &
# Expected: "Uvicorn running on http://0.0.0.0:8000"
```

### Check 17: Health Endpoint ✓
```bash
curl http://localhost:8000/health
# Expected: Healthy status response
```

### Check 18: API Documentation ✓
```bash
curl http://localhost:8000/docs 2>/dev/null | grep -i "swagger"
# Expected: HTML content with Swagger
# Or visit: http://localhost:8000/docs in browser
```

### Check 19: Query Endpoint (with documents) ✓
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Endee?", "session_id": "test"}'
# Expected: JSON response with answer and sources
```

### Check 20: Analytics Endpoint ✓
```bash
curl http://localhost:8000/analytics/stats
# Expected: JSON with system statistics
```

### Check 21: Query Optimization ✓
```bash
curl -X POST "http://localhost:8000/query/optimize" \
  -d "question=what%20is%20endee"
# Expected: Query analysis response
```

---

## Frontend UI Verification

### Check 22: Streamlit Running ✓
```bash
streamlit run frontend/streamlit_app.py &
# Expected: "You can now view your Streamlit app in your browser"
```

### Check 23: UI Accessible ✓
```bash
curl http://localhost:8501 2>/dev/null | head -20
# Expected: HTML content
# Or visit: http://localhost:8501 in browser
```

### Check 24: UI Responsive ✓
- Open browser to http://localhost:8501
- Expected: Page loads without errors
- Check: Chat interface visible

### Check 25: Ask Question via UI ✓
- Open http://localhost:8501
- Type: "What is Endee?"
- Click Send
- Expected: Answer appears with sources

---

## Integration Verification

### Check 26: End-to-End Query ✓
```bash
# Ask via API
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about vector databases", "session_id": "integration_test"}'

# Expected: 
# 1. Question is processed
# 2. Documents retrieved from Endee
# 3. Answer generated
# 4. Sources included
```

### Check 27: Cache Working ✓
```bash
# Ask same question twice
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Repeat question", "session_id": "test"}'

# Second request should be faster (cached)
# Check in analytics: curl http://localhost:0000/analytics/stats
```

### Check 28: Error Handling ✓
```bash
# Send invalid request
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'

# Expected: Error response (not crash)
```

---

## Performance Verification

### Check 29: Response Time ✓
```bash
time curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "First request"}'

# Expected: 3-5 seconds (first time) or <2 seconds (subsequent)
```

### Check 30: System Stability ✓
```bash
# Send multiple queries
for i in {1..5}; do
  curl -X POST "http://localhost:8000/ask" \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"Test query $i\"}" &
done
wait

# Expected: All succeed, no crashes, system stable
```

---

## Manual Testing Steps

### Test 1: Basic Query
1. Open http://localhost:8501
2. Type: "What is a vector database?"
3. Expected: Answer with sources
4. Result: ✓ or ✗

### Test 2: Follow-up Question
1. Type: "How does it work?"
2. Expected: Answer uses conversation context
3. Result: ✓ or ✗

### Test 3: New Session
1. New browser tab
2. Type: "Tell me about embeddings"
3. Expected: Different session, answer still correct
4. Result: ✓ or ✗

### Test 4: Upload Document (if implemented)
1. Look for upload button
2. Upload a .txt file
3. Run ingestion
4. Ask about new content
5. Expected: Answer references new document
6. Result: ✓ or ✗

---

## Log Verification

### Check Backend Logs
```bash
# Look for errors in backend terminal
# Expected: No [ERROR] or [CRITICAL] entries
# Each query should have logs:
# - Processing query
# - Retrieved N documents
# - Generated answer
# - Response sent
```

### Check Streamlit Logs
```bash
# Look for errors in Streamlit terminal
# Expected: No exceptions or crashes
# Each interaction should have logs
```

### Check Endee Logs
```bash
# Look for errors in Endee terminal
# Expected: Server running smoothly
# No connection errors
```

---

## File Integrity

### Check Key Files
```bash
# Verify all key files exist
ls -la backend/main.py
ls -la backend/endee_client.py
ls -la backend/rag_pipeline.py
ls -la scripts/ingest_documents.py
ls -la frontend/streamlit_app.py

# Expected: All files present with reasonable size
```

### Check Documentation
```bash
# Verify documentation exists
ls -la README.md
ls -la COMPLETE_SETUP.md
ls -la PROJECT_STATUS.md

# Expected: All files >500 lines
```

---

## System Health Summary

Create a summary file:
```bash
# Health check script (optional)
echo "=== SYSTEM HEALTH CHECK ===" > health_report.txt
echo "Time: $(date)" >> health_report.txt
echo "" >> health_report.txt
echo "Endee: $(curl -s http://localhost:8080/health)" >> health_report.txt
echo "API: $(curl -s http://localhost:8000/health)" >> health_report.txt
echo "Documents: $(python scripts/ingest_documents.py --dry-run 2>/dev/null | tail -1)" >> health_report.txt
echo "" >> health_report.txt
echo "Report saved to health_report.txt"
```

---

## Passing Criteria

### Minimum Requirements (Must Pass)
- [x] Endee server running and accessible
- [x] API server running and responding
- [x] Documents ingested into Endee
- [x] Can ask question and get answer
- [x] Answer includes sources
- [x] Web UI loads
- [x] No critical errors in logs

### Nice to Have (Enhancement)
- [x] Cache working and improving performance
- [x] Analytics endpoint working
- [x] Query optimization working
- [x] Multiple queries work correctly
- [x] System handles errors gracefully

---

## Troubleshooting During Verification

### If Check Fails

1. **Endee not responding**
   - Verify: `cd endee && ./run.sh`
   - Wait 5 seconds for startup
   - Try health check again

2. **API errors**
   - Check .env file has GEMINI_API_KEY
   - Verify all dependencies installed: `pip list`
   - Restart backend: Kill process and restart

3. **No documents retrieved**
   - Run ingestion: `python scripts/ingest_documents.py`
   - Verify completion: Check "vectors stored" message
   - Restart backend after ingestion

4. **Slow responses**
   - Normal for first query (model loading)
   - Subsequent queries should be faster
   - Check cache stats: `curl http://localhost:8000/analytics/stats`

5. **UI not loading**
   - Check port 8501 isn't blocked
   - Try different port: `streamlit run frontend/streamlit_app.py --server.port 8502`
   - Clear browser cache

---

## Success Confirmation

If all checks pass:

```
✓ All 30 verification checks passed
✓ System is fully functional
✓ Ready for use and deployment
✓ Can proceed to production

Signature: _________________
Date: _____________________
```

---

## Next Steps After Verification

1. **Use the System**
   - Open http://localhost:8501
   - Ask questions about your documents
   - Test with your own .txt files

2. **Monitor Performance**
   - Check analytics regularly
   - Monitor response times
   - Track cache effectiveness

3. **Scale Up**
   - Add more documents
   - Monitor resource usage
   - Optimize if needed

4. **Deploy**
   - Use Docker for production
   - Set up monitoring
   - Configure backups

---

## Support

If verification fails at any point:

1. Check COMPLETE_SETUP.md troubleshooting section
2. Review README.md for configuration
3. Check logs for specific error messages
4. Verify all prerequisites are met
5. Restart all components and try again

---

**Verification Document Complete**

Print this checklist and mark off each check as you verify it.
