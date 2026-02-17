"""
Application constants
"""

# Supported file types for document upload
SUPPORTED_FILE_TYPES = [".pdf", ".txt"]
SUPPORTED_MIME_TYPES = ["application/pdf", "text/plain"]

# Chunking configuration
CHUNK_SIZE = 1000  # characters
CHUNK_OVERLAP = 200  # characters

# Embedding configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536

# LLM configuration
LLM_MODEL = "gpt-5-mini"

RAG_TOP_K=5

# OpenAI Realtime API configuration
REALTIME_MODEL = "gpt-4o-mini-realtime-preview"
REALTIME_VOICE = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
REALTIME_TEMPERATURE = 0.8


# RAG configuration
RAG_TOP_K = 5  # Number of chunks to retrieve

# ChromaDB configuration
CHROMA_COLLECTION_NAME = "Voice_Ai"

# Document statuses
DOC_STATUS_UPLOADING = "uploading"
DOC_STATUS_PROCESSING = "processing"
DOC_STATUS_INDEXED = "indexed"
DOC_STATUS_FAILED = "failed"
