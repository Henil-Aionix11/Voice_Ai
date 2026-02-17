"""
RAG retrieval service for querying document knowledge base
"""
from typing import List, Dict
from app.services.embedding_service import embedding_service
from app.repositories.vector_repository import vector_repository
from app.config.constants import RAG_TOP_K
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RetrievalService:
    """Service for retrieving relevant context from ChromaDB"""
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
    
    async def retrieve_context(
        self,
        query: str,
        top_k: int = RAG_TOP_K
    ) -> List[Dict]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User query text
            top_k: Number of chunks to retrieve
        
        Returns:
            List of retrieved chunks with metadata
        """
        logger.info(f"Retrieving context for query: {query[:100]}...")
        
        try:
            # 1. Generate query embedding
            query_embeddings = await self.embedding_service.generate_embeddings([query])
            
            # 2. Query ChromaDB
            results = self.vector_repository.query(
                query_embeddings=query_embeddings,
                n_results=top_k
            )
            
            # 3. Format results
            retrieved_chunks = []
            
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):

                    retrieved_chunks.append({
                        "text": results['documents'][0][i],
                        "document_name": results['metadatas'][0][i]['document_name'],
                        "document_id": results['metadatas'][0][i]['document_id'],
                        "chunk_index": results['metadatas'][0][i]['chunk_index'],
                    })
            
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks")
            return retrieved_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []


# Create global instance
retrieval_service = RetrievalService()
