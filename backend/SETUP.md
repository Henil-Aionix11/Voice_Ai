# Backend Setup - Simplified Version

## Prerequisites

✅ Python 3.10+  
✅ OpenAI API Key  
❌ ~~PostgreSQL~~ (NOT NEEDED!)  

## Installation (3 Steps!)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-key-here
```

**That's all you need!** Other settings have good defaults.

### 3. Run the Application

**Terminal 1** - Start API Server:
```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2** - Start LiveKit Agent (optional for voice):
```bash
python -m app.agent
```

## Verify Setup

```bash
# Check API health
curl http://localhost:8000/health

# Open API docs
open http://localhost:8000/docs
```

## Quick Test

```bash
# Upload a document
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@test.pdf"

# List documents
curl http://localhost:8000/api/documents

# Get current prompt
curl http://localhost:8000/api/agent/prompt
```

## What's Different from Original?

### Removed ❌
- PostgreSQL database
- SQLAlchemy, asyncpg, alembic
- Database migrations
- Document metadata persistence

### Kept ✅
- ChromaDB (essential for RAG)
- All RAG functionality
- LiveKit voice integration
- OpenAI Realtime API
- Document upload/ingestion
- In-memory prompt storage

## Project Structure

```
backend/
├── app/
│   ├── config/          # Settings + in-memory config manager
│   ├── routes/          # Simplified API routes
│   ├── services/        # No DB dependencies
│   ├── repositories/    # ChromaDB only
│   ├── utils/           # File logging added
│   └── main.py          # Simplified startup
├── chroma_db/           # Auto-created (vector storage)
├── uploads/             # Auto-created (temp files)
├── logs/                # Auto-created (app logs)
└── requirements.txt     # Minimal dependencies
```

## Logs

Check application logs:
```bash
tail -f logs/app.log
tail -f logs/error.log
```

## Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### ChromaDB Error
```bash
rm -rf chroma_db/
# Restart the app
```

### Port Already in Use
```bash
# Change port in command
uvicorn app.main:app --reload --port 8001
```

## Next Steps

1. ✅ Backend is running
2. → Build frontend (React + LiveKit)
3. → Test voice flow
4. → Record demo video

**Perfect for interview demos!** 🎯
