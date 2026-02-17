"""
Document ingestion service for RAG pipeline (no database!)
"""
import os
from typing import Dict
from app.services.embedding_service import embedding_service
from app.repositories.vector_repository import vector_repository
from app.utils.chunking import ChunkingStrategy
from app.utils.file_utils import FileProcessor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class IngestionService:
    """Service for ingesting documents into the RAG system"""
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_repository = vector_repository
        self.chunking_strategy = ChunkingStrategy()
        self.file_processor = FileProcessor()
    
    async def ingest_document(
        self,
        file_path: str,
        document_id: str,
        filename: str
    ) -> Dict:
        """
        Ingest a document into ChromaDB
        
        Steps:
        1. Extract text from PDF/TXT
        2. Chunk text
        3. Generate embeddings
        4. Store in ChromaDB
        5. Delete source file
        
        Args:
            file_path: Path to the uploaded file
            document_id: Document UUID
            filename: Original filename
        
        Returns:
            Dict with ingestion results
        """
        try:
            logger.info(f"Starting ingestion for document {document_id}: {filename}")
            
            # 1. Extract text
            logger.info(f"Extracting text from {filename}")
            text = await self.file_processor.extract_text(file_path)
            
            if not text or len(text.strip()) == 0:
                raise ValueError("Extracted text is empty")
            
            # 2. Chunk text
            logger.info(f"Chunking text ({len(text)} characters)")
            chunks = self.chunking_strategy.chunk_text(
                text,
                metadata={
                    "document_id": document_id,
                    "document_name": filename
                }
            )
            
            logger.info(f"Created {len(chunks)} chunks")
            
            # 3. Generate embeddings
            logger.info("Generating embeddings")
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = await self.embedding_service.generate_embeddings(chunk_texts)
            
            # 4. Store in ChromaDB
            logger.info("Storing in ChromaDB")
            self.vector_repository.add_chunks(
                embeddings=embeddings,
                chunks=chunks,
                document_id=document_id
            )
            
            # 5. Delete the file after successful ingestion
            logger.info(f"Deleting source file: {file_path}")
            self.file_processor.delete_file(file_path)
            
            logger.info(f"Successfully ingested document {document_id}")
            
            return {
                "document_id": document_id,
                "filename": filename,
                "total_chunks": len(chunks),
                "status": "indexed"
            }
            
        except Exception as e:
            logger.error(f"Error ingesting document {document_id}: {e}")
            
            # Still try to clean up the file
            if os.path.exists(file_path):
                self.file_processor.delete_file(file_path)
            
            raise


# Create global instance
ingestion_service = IngestionService()
