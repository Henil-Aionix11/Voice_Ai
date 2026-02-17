# Voice AI - Real-Time Voice Agent with RAG

This project implements a real-time voice AI agent that can converse with users over WebRTC (via LiveKit) and answer questions using RAG (Retrieval Augmented Generation) over uploaded documents.

## Project Structure

```
Voice_Ai/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── config/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── utils/
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/         # React frontend (Coming soon)
    └── README.md
```

## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the backend:
```bash
uvicorn app.main:app --reload
```

5. Run the LiveKit agent (in a separate terminal):
```bash
python -m app.agent
```

See [backend/README.md](backend/README.md) for detailed instructions.

## Features

- ✅ Real-time voice conversations via LiveKit
- ✅ Speech-to-Text and Text-to-Speech using OpenAI Realtime API
- ✅ RAG with document upload (PDF, TXT)
- ✅ Vector storage with ChromaDB
- ✅ Customizable AI agent prompts
- ✅ Live transcripts (both user and agent)

## Tech Stack

- **Backend**: FastAPI, PostgreSQL, ChromaDB
- **Voice**: LiveKit, OpenAI Realtime API
- **AI**: OpenAI GPT-4o-mini, text-embedding-3-small
- **Frontend**: React (TypeScript) + LiveKit React SDK

## Documentation

- [Implementation Plan](docs/implementation_plan.md)
- [Backend README](backend/README.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## License

MIT
