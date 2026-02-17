"""
Repositories package (ChromaDB only - no database!)
"""
from app.repositories.vector_repository import VectorRepository, vector_repository

__all__ = [
    "VectorRepository",
    "vector_repository"
]
