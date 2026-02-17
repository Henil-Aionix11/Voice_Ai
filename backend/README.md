# Voice AI Backend - Simplified ✨

**Real-Time Voice AI Agent with RAG - No Database Setup Required!**

## Features

- 🎙️ **Real-time voice** via LiveKit + OpenAI Realtime API
- 📚 **RAG** with ChromaDB (local vector storage)
- 📄 **Document upload** (PDF, TXT) with auto-ingestion
- 🤖 **Customizable AI prompts** (in-memory)
- 📝 **File logging** to `logs/` directory

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

**Required**:
- `OPENAI_API_KEY` - Your OpenAI API key

**Optional** (defaults work for local dev):
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- `CHROMA_DB_PATH`, `UPLOAD_DIR`

### 3. Run Backend

Terminal 1 - API Server:
```bash
uvicorn app.main:app --reload --port 8000
```

Terminal 2 - LiveKit Agent:
```bash
python -m app.agent
```

**That's it!** No PostgreSQL needed! 🎉

## API Endpoints

### Documents
- `POST /api/documents/upload` - Upload PDF/TXT
- `GET /api/documents` - List all documents
- `DELETE /api/documents/{id}` - Delete document

### Agent Prompt
- `GET /api/agent/prompt` - Get current prompt
- `PUT /api/agent/prompt` - Update prompt (in-memory)
- `POST /api/agent/prompt/reset` - Reset to default

### LiveKit
- `POST /api/livekit/token` - Generate access token

## Architecture

```
User Upload → Ingest → ChromaDB
                ↓
User Voice → LiveKit → OpenAI Realtime → RAG → Response
```

**Storage**:
- ✅ ChromaDB - Document vectors (persistent)
- ✅ In-memory - Agent prompt (session-based)
- ✅ File logs - `logs/app.log`, `logs/error.log`

**No PostgreSQL required!**

## Project Structure

```
backend/
├── app/
│   ├── config/          # Settings, constants, prompts
│   ├── routes/          # API routes (documents, agent, livekit)
│   ├── services/        # Core services (RAG, embeddings, etc.)
│   ├── repositories/    # ChromaDB only
│   ├── utils/           # Helpers (logging, chunking, files)
│   └── main.py          # FastAPI app
├── requirements.txt     # Dependencies (no SQLAlchemy!)
└── .env.example
```

## Dependencies

**Core**:
- FastAPI, Uvicorn
- OpenAI (embeddings, LLM, Realtime API)
- ChromaDB (vector store)
- LangChain (document processing)
- LiveKit (voice infrastructure)

**No database ORM needed!**

## Logging

All logs are written to:
- `logs/app.log` - All application logs
- `logs/error.log` - Errors only

## Development

API Documentation: http://localhost:8000/docs

Health Check: http://localhost:8000/health

## Demo Ready ✅

This simplified version is perfect for interviews:
- ✅ Easy setup (just Python + OpenAI key)
- ✅ No database installation
- ✅ Works out of the box
- ✅ All core features included

## License

MIT
