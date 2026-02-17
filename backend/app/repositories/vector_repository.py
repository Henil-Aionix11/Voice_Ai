"""
ChromaDB vector repository
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
from app.config.settings import settings as app_settings
from app.config.constants import CHROMA_COLLECTION_NAME
from app.utils.logger import get_logger

logger = get_logger(__name__)


class VectorRepository:
    """
    ChromaDB vector repository for storing and querying document embeddings
    """
    
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        logger.info(f"Initializing ChromaDB at {app_settings.CHROMA_DB_PATH}")
        
        # Use PersistentClient to save data between restarts
        self.client = chromadb.PersistentClient(
            path=app_settings.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"ChromaDB collection '{CHROMA_COLLECTION_NAME}' ready with {self.collection.count()} existing chunks")
    
    def add_chunks(
        self,
        embeddings: List[List[float]],
        chunks: List[Dict],
        document_id: str
    ):
        """
        Add chunks with embeddings to ChromaDB
        
        Args:
            embeddings: List of embedding vectors
            chunks: List of chunk dicts with 'text' and 'metadata' keys
            document_id: Document UUID
        """
        ids = [f"{document_id}_{chunk['metadata']['chunk_index']}" 
               for chunk in chunks]
        
        documents = [chunk["text"] for chunk in chunks]
        
        metadatas = [
            {
                "document_id": str(document_id),
                "document_name": chunk["metadata"]["document_name"],
                "chunk_index": chunk["metadata"]["chunk_index"],
                "total_chunks": chunk["metadata"]["total_chunks"]
            }
            for chunk in chunks
        ]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        logger.info(f"Added {len(chunks)} chunks to ChromaDB for document {document_id}")
    
    def query(
        self,
        query_embeddings: List[List[float]],
        n_results: int = 5
    ) -> Dict:
        """
        Query ChromaDB for similar chunks
        
        Args:
            query_embeddings: Query embedding vector
            n_results: Number of results to return
        
        Returns:
            ChromaDB query results
        """
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        
        logger.info(f"Retrieved {len(results['ids'][0])} chunks from ChromaDB")
        return results
    
    def delete_by_document_id(self, document_id: str):
        """Delete all chunks for a specific document"""
        # Get all IDs with this document_id in metadata
        results = self.collection.get(
            where={"document_id": str(document_id)}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")


# Create global instance
vector_repository = VectorRepository()
