# Installation & Running Summary

Complete reference for installing and running the Endee AI Knowledge Assistant.

---

## TL;DR (Too Long; Didn't Read)

**Just want to run it?**

```bash
# Step 1: Get API key (2 minutes)
# Visit: https://makersuite.google.com/app/apikey

# Step 2: Run this one command
./start.sh

# Step 3: Open in browser
# Visit: http://localhost:8501

# Done! 🎉
```

That's literally all you need to do. The script handles everything else.

---

## Three Installation Methods

### Method 1: Automated Script (EASIEST) ⭐⭐⭐

**Time:** 5 minutes  
**Difficulty:** Very Easy  
**Requirements:** Python 3.9+ (already installed on most systems)

```bash
# Step 1: Make script executable (first time only)
chmod +x start.sh

# Step 2: Run the script
./start.sh

# Step 3: The script asks for your Gemini API key
# Paste it when prompted

# Step 4: Script automatically starts everything
# - Backend server
# - Frontend interface
# - Opens browser

# Done! Open http://localhost:8501
```

**What the script does automatically:**
- Creates virtual environment
- Installs all dependencies
- Configures environment
- Starts FastAPI backend
- Starts Streamlit frontend
- Opens browser automatically

**Pros:** Easiest, fully automated, no thinking required
**Cons:** Less transparent, harder to troubleshoot if something fails

---

### Method 2: Manual Installation (DETAILED) ⭐⭐

**Time:** 15 minutes  
**Difficulty:** Easy to Medium  
**Requirements:** Python 3.9+, basic command line skills

#### Step 1: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Step 2: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all packages
pip install -r requirements.txt

# Takes 2-3 minutes
```

#### Step 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit the file
nano .env  # macOS/Linux
# or
notepad .env  # Windows
```

Add your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

#### Step 4: Start Backend (Terminal 1)

```bash
# Activate if not already
source venv/bin/activate

# Start FastAPI
python -m uvicorn backend.main:app --reload

# You'll see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

#### Step 5: Start Frontend (Terminal 2)

Open a new terminal:

```bash
# Activate virtual environment
source venv/bin/activate

# Start Streamlit
streamlit run frontend/streamlit_app.py

# You'll see:
# Local URL: http://localhost:8501
```

#### Step 6: Access

- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

**Pros:** Transparent, easy to troubleshoot, you understand each step
**Cons:** More steps, more thinking required

---

### Method 3: Docker (MODERN) ⭐⭐⭐

**Time:** 10 minutes  
**Difficulty:** Easy  
**Requirements:** Docker installed ([Get it here](https://www.docker.com/products/docker-desktop))

```bash
# Step 1: Start with docker-compose
docker-compose -f docker-compose-app.yml up

# Step 2: Docker builds image and starts services
# Takes 2-3 minutes on first run

# Step 3: You'll see:
# backend_1 | INFO: Uvicorn running on http://0.0.0.0:8000
# streamlit_1 | Local URL: http://localhost:8501

# Step 4: Open browser
# http://localhost:8501
```

**Stopping Docker:**
```bash
# Stop services
docker-compose -f docker-compose-app.yml down

# View logs
docker-compose -f docker-compose-app.yml logs -f
```

**Pros:** No installation mess, works consistently, professional approach
**Cons:** Requires Docker, slightly more complex if you've never used Docker

---

## Before You Start: Checklist

Before installing, verify you have:

- [ ] **Gemini API Key** (get free one from https://makersuite.google.com/app/apikey)
- [ ] **Python 3.9+** (check with `python --version`)
  
  OR
  
- [ ] **Docker** (check with `docker --version`)

- [ ] **2 GB disk space** minimum
- [ ] **4 GB RAM** minimum (8 GB recommended)
- [ ] **Internet connection**

Missing something? No problem:

**For API Key:**
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key
5. You're done - free tier is generous!

**For Python:**
```bash
# Check version
python --version  # Should be 3.9+

# If not installed, download from: https://python.org
```

---

## Getting Your Gemini API Key (Detailed)

The only thing you MUST do before starting:

1. **Visit:** https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click** "Create API Key"
4. **Copy** the key shown
5. **Save it somewhere** safe

**Generating the key takes 2 minutes maximum.**

The free tier includes:
- 60 requests per minute
- Unlimited daily requests (subject to account quota)
- Full Gemini capabilities

That's enough for most use cases!

---

## Quick Comparison

| Aspect | Script | Manual | Docker |
|--------|--------|--------|--------|
| **Time** | 5 min | 15 min | 10 min |
| **Difficulty** | Very Easy | Easy | Easy |
| **Transparent** | ❌ | ✅ | ⚠️ |
| **Troubleshooting** | Hard | Easy | Medium |
| **Production-ready** | ❌ | ✅ | ✅ |
| **Best for** | First-time | Learning | Production |

**Recommendation:** Use the script first. If it doesn't work, try manual.

---

## After Installation: What to Do

### Access Points

After starting, you can access:

```
Web Interface: http://localhost:8501
API Docs:      http://localhost:8000/docs
API ReDoc:     http://localhost:8000/redoc
Health Check:  http://localhost:8000/health
```

### First Things to Try

1. **Ask a question without documents:**
   - Type: "What can you help me with?"
   - System explains capabilities

2. **Load sample documents:**
   ```bash
   python -m scripts.ingest_documents --mode sample
   ```
   - Then ask: "What documents do I have?"

3. **Upload your own document:**
   - Click "📚 Document Upload"
   - Select a PDF or text file
   - Click "📤 Upload & Ingest"
   - Ask questions about it

---

## Troubleshooting Installation

### "Port 8000 is already in use"

**Problem:** Something else is using port 8000

**Fix:**
```bash
# macOS/Linux - find what's using it
lsof -i :8000

# macOS/Linux - kill it
kill -9 <PID>

# OR use a different port
python -m uvicorn backend.main:app --port 8001
```

### "ModuleNotFoundError: No module named..."

**Problem:** Dependencies not installed

**Fix:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "GEMINI_API_KEY is not set"

**Problem:** API key not configured

**Fix:**
1. Get key: https://makersuite.google.com/app/apikey
2. Edit `.env` file
3. Add: `GEMINI_API_KEY=your_key_here`
4. Restart the application

### Streamlit won't load

**Problem:** Frontend not responding

**Fix:**
```bash
# Clear cache
streamlit cache clear

# Restart
streamlit run frontend/streamlit_app.py --logger.level=debug
```

### "Python not found" / "Command not found"

**Problem:** Python not installed or not in PATH

**Fix:**
- Check Python is installed: `python --version`
- If not, download from: https://python.org
- Make sure "Add to PATH" is checked during installation

### More issues?

See detailed troubleshooting: [HOW_TO_RUN.md#troubleshooting](./HOW_TO_RUN.md#troubleshooting)

---

## Verification Checklist

After installation, verify everything works:

- [ ] http://localhost:8501 opens (web interface)
- [ ] You can type in the chat box
- [ ] System responds to your questions
- [ ] http://localhost:8000/docs works (API docs)
- [ ] You can upload files
- [ ] System shows response details

If all checkboxes are ✅, you're ready to use it!

---

## Next Steps

### Right After Installation

1. **Upload a document:** Use "📚 Document Upload"
2. **Ask a question:** Try "What did I upload?"
3. **Explore features:** Click around the interface
4. **Check API:** Visit http://localhost:8000/docs

### Next Hour

1. **Read documentation:** [START_HERE.md](./START_HERE.md)
2. **Upload more documents**
3. **Explore the API**
4. **Customize settings** (optional)

### Next Day

1. **Read detailed docs:** [DEVELOPMENT.md](./DEVELOPMENT.md)
2. **Plan customizations**
3. **Start building**

---

## System Requirements Reference

### Minimum
- Python 3.9+ or Docker
- 4 GB RAM
- 2 GB disk space
- Internet connection

### Recommended
- Python 3.10+
- 8 GB RAM
- 5 GB disk space
- SSD for faster performance
- Good internet connection

### Operating Systems
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)
- ✅ Windows (10, 11 with WSL2 recommended)

---

## Environment Setup (Technical Details)

### Virtual Environment (Python Only)

What it does:
- Isolates project dependencies
- Prevents conflicts with system Python
- Makes the project portable

Why it's important:
- Different projects may need different versions
- System Python may have permissions issues
- Easy cleanup (just delete the folder)

### Docker (Alternative)

What it does:
- Packages everything in a container
- No Python installation needed
- Consistent across all machines

Why use it:
- Identical behavior everywhere
- No dependency conflicts
- Production-standard approach

---

## Common Commands Reference

### Virtual Environment Management

```bash
# Create environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate (all platforms)
deactivate

# Check if activated
# You should see (venv) in your prompt
```

### Dependency Installation

```bash
# Install from requirements
pip install -r requirements.txt

# Install specific package
pip install streamlit

# Upgrade pip
pip install --upgrade pip

# List installed packages
pip list
```

### Running the Application

```bash
# Start backend
python -m uvicorn backend.main:app --reload

# Start frontend
streamlit run frontend/streamlit_app.py

# Run utility script
python -m scripts.ingest_documents --mode sample

# Health check
curl http://localhost:8000/health
```

### Docker Commands

```bash
# Start services
docker-compose -f docker-compose-app.yml up

# Stop services
docker-compose -f docker-compose-app.yml down

# View logs
docker-compose -f docker-compose-app.yml logs -f

# Rebuild image
docker-compose -f docker-compose-app.yml up --build
```

---

## Installation FAQ

**Q: Do I need to install Endee?**
A: No! The system works without it. Endee is optional.

**Q: Is the Gemini API free?**
A: Yes! Free tier has 60 requests/minute. No credit card needed.

**Q: Can I run this on Windows?**
A: Yes! Use WSL2 for best experience, or run on Windows directly.

**Q: Do I need Docker?**
A: No! It's optional. Use the script or manual method instead.

**Q: What if installation fails?**
A: See troubleshooting section or [HOW_TO_RUN.md](./HOW_TO_RUN.md#troubleshooting)

**Q: Can I uninstall it?**
A: Yes! Just delete the project folder. Virtual environment is isolated.

**Q: Will it mess up my system?**
A: No! Virtual environment keeps everything isolated.

---

## Quick Start Templates

Copy and paste based on your choice:

### Template 1: Script Method
```bash
chmod +x start.sh
./start.sh
# Follow prompts
```

### Template 2: Manual Method
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key
python -m uvicorn backend.main:app --reload
# In another terminal:
streamlit run frontend/streamlit_app.py
```

### Template 3: Docker Method
```bash
docker-compose -f docker-compose-app.yml up
# That's it!
```

---

## Still Stuck?

1. **Check:** [HOW_TO_RUN.md#troubleshooting](./HOW_TO_RUN.md#troubleshooting)
2. **Read:** [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
3. **Learn:** [START_HERE.md](./START_HERE.md)
4. **Explore:** [VISUAL_GUIDE.md](./VISUAL_GUIDE.md)

---

## Success Criteria

You're successful when:

1. ✅ Application starts without errors
2. ✅ http://localhost:8501 opens in browser
3. ✅ You can type in the chat
4. ✅ System responds to questions
5. ✅ You can upload documents

**All checkmarks?** Congratulations! You're ready to use it! 🎉

---

## Your Command

Pick one and run it:

```bash
# Easiest - Automated script
./start.sh

# OR - Manual setup
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# OR - Docker
docker-compose -f docker-compose-app.yml up
```

Then visit: **http://localhost:8501**

---

**That's all you need to know!**

Start now with your chosen method.

Need more details? See [HOW_TO_RUN.md](./HOW_TO_RUN.md)

🚀 **Let's go!**
