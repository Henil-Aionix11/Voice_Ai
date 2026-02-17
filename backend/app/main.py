"""
Main FastAPI application (simplified - no database!)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from app.config.settings import settings
from app.routes import documents, agent, livekit, chat
from app.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting Voice AI Backend...")
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"Upload directory ready: {settings.UPLOAD_DIR}")
    
    # Ensure ChromaDB directory exists
    os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
    logger.info(f"ChromaDB directory ready: {settings.CHROMA_DB_PATH}")
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    logger.info("Logs directory ready: ./logs")
    
    logger.info("Backend started successfully!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Voice AI Backend...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Real-Time Voice AI Agent with RAG (Simplified - No Database!)",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix=settings.API_V1_PREFIX)
app.include_router(agent.router, prefix=settings.API_V1_PREFIX)
app.include_router(livekit.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Voice AI Backend API",
        "version": "1.0.0",
        "status": "running",
        "features": ["RAG", "LiveKit Voice", "OpenAI Realtime API"],
        "database": "ChromaDB (No PostgreSQL needed!)"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "voice-ai-backend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=settings.DEBUG
    )
