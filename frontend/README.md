# Voice AI Frontend

Modern React frontend for real-time voice AI agent with RAG capabilities.

## Features

✅ Real-time voice conversation over WebRTC (LiveKit)  
✅ Document upload & management (PDF, TXT)  
✅ Customizable agent prompts  
✅ Live conversation transcript  
✅ RAG source visualization  
✅ Dark theme UI with glassmorphism  

## Tech Stack

- **React 18** + TypeScript
- **Vite** - Fast build tool
- **TailwindCSS** - Utility-first CSS
- **LiveKit** - WebRTC infrastructure
- **Zustand** - State management
- **Axios** - HTTP client

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file:

```env
VITE_API_URL=http://localhost:5000
VITE_LIVEKIT_URL=ws://localhost:7880
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Usage

### 1. Upload Documents
1. Navigate to "Documents" tab
2. Drag & drop or browse to upload PDF/TXT files
3. Wait for ingestion to complete

### 2. Customize Prompt (Optional)
1. Navigate to "Prompt" tab  
2. Edit the system prompt
3. Click "Save Changes"

### 3. Start Voice Call
1. Navigate to "Voice Call" tab
2. Click "Start Call"
3. Start speaking when connected
4. View live transcript on the right
5. See RAG sources when agent uses documents

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── VoiceCall/      # Voice room & controls
│   │   ├── Documents/       # Upload & list
│   │   ├── Agent/           # Prompt editor
│   │   └── RAG/             # Sources panel
│   ├── services/            # API clients
│   ├── stores/              # State management
│   ├── types/               # TypeScript types
│   ├── App.tsx              # Main component
│   └── main.tsx             # Entry point
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## Build for Production

```bash
npm run build
```

Build output will be in `dist/` directory.

## Requirements

- Node.js 18+
- Backend running on port 5000
- LiveKit server running on port 7880

## Troubleshooting

### Connection Issues
- Ensure backend is running (`cd backend && uvicorn app.main:app --port 5000`)
- Ensure LiveKit server is running
- Check browser console for errors

### No Audio
- Check microphone permissions
- Verify LiveKit URL in `.env`
- Test microphone in browser settings
