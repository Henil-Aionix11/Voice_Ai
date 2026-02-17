# Voice AI - Real-Time Voice Agent with RAG

**Enterprise-Grade Real-Time Voice AI Assistant with Document Understanding**

A production-ready voice AI system that enables natural conversations with RAG (Retrieval-Augmented Generation) capabilities. Users can upload documents and have real-time voice conversations where the AI agent intelligently retrieves and references relevant information.

---

## 🎯 Key Features

- 🎙️ **Real-Time Voice Conversations** - Low-latency voice interaction via WebRTC (LiveKit)
- 🤖 **OpenAI Realtime API** - Speech-to-Speech with GPT-4o-mini  
- 📚 **RAG Integration** - Upload documents (PDF, TXT) and query them via voice
- 📝 **Live Transcription** - Real-time transcription display for both user and agent
- 🎨 **Modern UI** - Responsive dark-theme interface with glassmorphism
- 🔧 **Customizable** - Editable AI agent prompts and behaviors
- 📊 **Source Visualization** - See which document chunks the AI is referencing

---

## 🏗️ Architecture

### System Components

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │◄────►│   Backend    │◄────►│  ChromaDB   │
│  (React)    │      │  (FastAPI)   │      │  (Vectors)  │
└──────┬──────┘      └──────┬───────┘      └─────────────┘
       │                    │
       └────────┬───────────┘
                │
         ┌──────▼───────┐
         │   LiveKit    │
         │   Server     │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  LiveKit     │
         │  Agent       │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │   OpenAI     │
         │ Realtime API │
         └──────────────┘
```

### Data Flow

```
1. Document Upload:
   User → Frontend → Backend → Document Processing → Embeddings → ChromaDB

2. Voice Conversation:
   User Speech → LiveKit → Agent → OpenAI Realtime API
                    ↓
   Query → RAG Service → ChromaDB → Context Retrieval
                    ↓
   Context + Response → OpenAI → Agent → LiveKit → User
```

---

## 🧠 AI Models & Configuration

### Models Used

| Purpose | Model | Configuration |
|---------|-------|---------------|
| **Voice Assistant** | `gpt-4o-mini-realtime-preview` | Temperature: 0.8, Voice: alloy |
| **Embeddings** | `text-embedding-3-small` | Dimensions: 1536 |
| **Chat (Fallback)** | `gpt-5-mini` | For non-realtime operations |

### RAG Configuration

- **Chunking**: 1000 characters per chunk, 200 character overlap
- **Top-K Retrieval**: 5 most relevant chunks per query
- **Vector Store**: ChromaDB (persistent local storage)
- **Collection**: `Voice_Ai`

---

## 📁 Project Structure

```
Voice_Ai/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── agent.py           # LiveKit agent entry point
│   │   ├── main.py            # FastAPI application
│   │   ├── config/
│   │   │   ├── constants.py   # Configuration constants
│   │   │   ├── prompt.py      # AI agent prompts
│   │   │   └── settings.py    # Environment settings
│   │   ├── routes/
│   │   │   ├── agent_routes.py      # Prompt management
│   │   │   ├── document_routes.py   # Document upload/management
│   │   │   └── livekit_routes.py    # LiveKit token generation
│   │   ├── services/
│   │   │   ├── livekit_agent_service.py  # Agent logic
│   │   │   ├── embedding_service.py       # OpenAI embeddings
│   │   │   ├── retrieval_service.py       # RAG retrieval
│   │   │   └── document_service.py        # Document processing
│   │   ├── repositories/
│   │   │   └── vector_repository.py       # ChromaDB interface
│   │   └── utils/
│   │       ├── text_chunking.py           # Document chunking
│   │       └── file_utils.py              # File operations
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── VoiceCall/      # Voice room & controls
│   │   │   ├── Documents/       # Document management
│   │   │   ├── Agent/           # Prompt editor
│   │   │   └── RAG/             # Source visualization
│   │   ├── services/            # API clients
│   │   ├── stores/              # Zustand state management
│   │   └── types/               # TypeScript definitions
│   ├── package.json
│   └── .env.example
│
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker** (for LiveKit server)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Installation

#### 1. Clone Repository

```bash
git clone <your-repo-url>
cd Voice_Ai
```

#### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required
OPENAI_API_KEY=sk-your-openai-key-here

# Optional (defaults work for local development)
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
CHROMA_DB_PATH=./chroma_db
UPLOAD_DIR=./uploads
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install Node dependencies
npm install

# Configure environment
cp .env.example .env
```

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:5000
VITE_LIVEKIT_URL=ws://localhost:7880
```

---

## ▶️ Running the Application

The application requires **4 services** to run simultaneously. Open 4 separate terminal windows:

### Terminal 1: LiveKit Server (Docker)

```bash
docker run --rm -p 7880:7880 -p 7881:7881 livekit/livekit-server --dev --keys "devkey: secret"
```

**What it does**: Provides WebRTC infrastructure for real-time voice communication

### Terminal 2: LiveKit Agent Worker

```bash
cd backend

# Windows
set LIVEKIT_URL=ws://localhost:7880
set LIVEKIT_API_KEY=devkey
set LIVEKIT_API_SECRET=secret
set OPENAI_API_KEY=your_openai_key_here
python -m app.agent start

# Linux/Mac
export LIVEKIT_URL=ws://localhost:7880
export LIVEKIT_API_KEY=devkey
export LIVEKIT_API_SECRET=secret
export OPENAI_API_KEY=your_openai_key_here
python -m app.agent start
```

**What it does**: Runs the AI agent that handles voice interactions and RAG

### Terminal 3: Backend API Server

```bash
cd backend
uvicorn app.main:app --port 5000 --reload
```

**What it does**: Serves the REST API for document management and LiveKit tokens

### Terminal 4: Frontend Development Server

```bash
cd frontend
npm run dev
```

**What it does**: Runs the React development server

---

## 🎮 Usage

### Access the Application

Open your browser and navigate to: **http://localhost:3000**

### 1. Upload Documents

1. Click on the **"Documents"** tab
2. Drag & drop or browse to select PDF/TXT files
3. Wait for processing to complete (you'll see status change to "Indexed")

### 2. Customize Agent (Optional)

1. Click on the **"Prompt"** tab
2. Edit the system prompt to customize agent behavior
3. Click **"Save Changes"**
4. Or click **"Reset to Default"** to restore original prompt

### 3. Start Voice Conversation

1. Click on the **"Voice Call"** tab
2. Click **"Start Call"** - agent will connect
3. Allow microphone access when prompted
4. Start speaking naturally
5. View live transcript on the right side
6. See RAG sources when the agent references documents

### 4. View RAG Sources

When the agent uses your documents to answer:
- **Right panel** shows which document chunks were retrieved
- Each source displays:
  - Document name
  - Relevant text excerpt
  - Relevance score

---

## 🔧 Configuration

### Backend Configuration

All configuration constants are in `backend/app/config/constants.py`:

```python
# Embedding Model
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536

# Realtime Voice Model  
REALTIME_MODEL = "gpt-4o-mini-realtime-preview"
REALTIME_VOICE = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
REALTIME_TEMPERATURE = 0.8

# Document Processing
CHUNK_SIZE = 1000           # Characters per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
SUPPORTED_FILE_TYPES = [".pdf", ".txt"]

# RAG Retrieval
RAG_TOP_K = 5              # Number of chunks to retrieve
```

### Frontend Configuration

Environment variables in `frontend/.env`:

```env
VITE_API_URL=http://localhost:5000      # Backend API URL
VITE_LIVEKIT_URL=ws://localhost:7880     # LiveKit WebSocket URL
```

---

## 📡 API Endpoints

### Documents Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents/upload` | Upload PDF or TXT file |
| `GET` | `/api/documents` | List all uploaded documents |
| `DELETE` | `/api/documents/{id}` | Delete a document |

### Agent Configuration

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/agent/prompt` | Get current system prompt |
| `PUT` | `/api/agent/prompt` | Update system prompt |
| `POST` | `/api/agent/prompt/reset` | Reset to default prompt |

### LiveKit Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/livekit/token` | Generate access token for room |

### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | API health check |

**Interactive API Documentation**: http://localhost:5000/docs (when backend is running)

---

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **LiveKit** - WebRTC infrastructure
- **LiveKit Agents** - AI agent framework
- **OpenAI** - GPT models and Realtime API
- **ChromaDB** - Vector database
- **LangChain** - Document processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend

- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **TailwindCSS** - Utility-first CSS
- **LiveKit Components React** - Pre-built voice components
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Icon library

---

## 📦 Dependencies

### Backend (`requirements.txt`)

```txt
# Core API
fastapi
uvicorn[standard]
python-multipart

# Validation & Config
pydantic
pydantic-settings
python-dotenv

# OpenAI (LLM + Realtime)
openai

# RAG / Documents
langchain
langchain-community
chromadb
pymupdf

# LiveKit (WebRTC + Agent)
livekit
livekit-agents
livekit-plugins-openai

# Utilities
aiofiles
```

### Frontend (`package.json`)

```json
{
  "dependencies": {
    "@headlessui/react": "^1.7.18",
    "@livekit/components-react": "^2.0.7",
    "axios": "^1.6.7",
    "livekit-client": "^2.0.7",
    "react": "^18.2.0",
    "zustand": "^4.5.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3",
    "vite": "^7.3.1"
  }
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. LiveKit Connection Failed

**Problem**: Frontend can't connect to LiveKit server

**Solution**:
- Ensure LiveKit Docker container is running
- Check that port 7880 is accessible
- Verify `VITE_LIVEKIT_URL` in frontend `.env` matches server URL

#### 2. Agent Not Responding

**Problem**: Voice call connects but agent doesn't respond

**Solution**:
- Check agent worker terminal for errors
- Verify `OPENAI_API_KEY` is set correctly
- Ensure agent worker has the same LiveKit credentials as server
- Check agent worker logs for OpenAI API errors

#### 3. Document Upload Fails

**Problem**: Files won't upload or process

**Solution**:
- Check backend logs for errors
- Verify file is PDF or TXT format
- Ensure backend has write permissions to `uploads/` directory
- Check ChromaDB path is accessible

#### 4. No Audio in Voice Call

**Problem**: Can't hear agent or agent can't hear you

**Solution**:
- Grant microphone permissions in browser
- Check browser console for WebRTC errors
- Test microphone in browser settings
- Try a different browser (Chrome/Edge recommended)

#### 5. Empty Input Error

**Problem**: Embedding API errors with empty input

**Solution**:
- This is usually harmless (background noise detected as speech)
- The system automatically skips empty transcripts
- If persistent, check microphone sensitivity

### Logs & Debugging

**Backend Logs**: Check terminal running `uvicorn` and agent worker

**Frontend Logs**: Open browser DevTools (F12) → Console tab

**LiveKit Logs**: Check Docker container output

---

## 🔒 Security Considerations

### For Production Deployment

1. **Environment Variables**
   - Never commit `.env` files to version control
   - Use secure secret management (AWS Secrets Manager, Azure Key Vault, etc.)
   
2. **LiveKit Credentials**
   - Replace `devkey: secret` with strong, random values
   - Use the official LiveKit Cloud for production
   
3. **API Keys**
   - Rotate OpenAI API keys regularly
   - Set usage limits on OpenAI dashboard
   
4. **CORS**
   - Configure proper CORS origins in FastAPI
   - Don't use `allow_origins=["*"]` in production
   
5. **File Upload**
   - Implement file size limits
   - Scan uploaded files for malware
   - Use cloud storage (S3, Azure Blob) instead of local storage

---

## 📈 Performance Optimization

### Recommendations for Scale

1. **Use LiveKit Cloud** - Production-grade infrastructure
2. **Deploy Backend** - Use Gunicorn with multiple workers
3. **CDN for Frontend** - Serve static files via CDN
4. **Vector DB** - Consider Pinecone or Weaviate for large-scale
5. **Caching** - Implement Redis for embedding cache
6. **Load Balancing** - Use NGINX or cloud load balancers

---

## 🚢 Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/` - serve with any static hosting (Netlify, Vercel, S3+CloudFront, etc.)

### Deploy Backend

```bash
cd backend

# Using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000

# Or Docker
docker build -t voice-ai-backend .
docker run -p 5000:5000 --env-file .env voice-ai-backend
```

### Environment Setup

Ensure all environment variables are set in your production environment (AWS ECS, Heroku, Railway, etc.)

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙋 Support

For questions or issues:
- Check the [Troubleshooting](#-troubleshooting) section
- Review [LiveKit Documentation](https://docs.livekit.io/)
- Review [OpenAI Realtime API Docs](https://platform.openai.com/docs/guides/realtime)

---

## 🎉 Credits

Built with:
- [LiveKit](https://livekit.io/) - Real-time communication platform
- [OpenAI](https://openai.com/) - AI models and APIs
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [React](https://react.dev/) - Frontend framework

---

**Ready to experience real-time AI conversations with document understanding!** 🎯🎙️
