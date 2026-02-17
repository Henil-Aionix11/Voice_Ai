"""
Simplified document management service without database
Uses ChromaDB metadata for tracking documents
"""
import os
import uuid
from typing import List, Dict
from fastapi import UploadFile
from app.services.ingestion_service import ingestion_service
from app.repositories.vector_repository import vector_repository
from app.config.settings import settings
from app.utils.file_utils import FileProcessor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentService:
    """Service for document management operations (no database!)"""
    
    def __init__(self):
        self.ingestion_service = ingestion_service
        self.file_processor = FileProcessor()
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def upload_documents(self, files: List[UploadFile]) -> Dict:
        """
        Handle multiple document uploads and ingestion
        
        Args:
            files: List of uploaded files
        
        Returns:
            Dict with successful and failed uploads
        """
        successful = []
        failed = []
        
        for file in files:
            try:
                result = await self.upload_document(file)
                successful.append(result)
            except Exception as e:
                logger.error(f"Failed to upload {file.filename}: {e}")
                failed.append({
                    "filename": file.filename,
                    "error": str(e)
                })
        
        return {
            "successful": successful,
            "failed": failed
        }
    
    async def upload_document(self, file: UploadFile) -> Dict:
        """
        Handle document upload and ingestion
        
        Args:
            file: Uploaded file
        
        Returns:
            Dict with document information
        """
        # Validate file type
        if not self.file_processor.is_supported_file(file.filename):
            raise ValueError(f"Unsupported file type. Supported: PDF, TXT")
        
        # Check file size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise ValueError(f"File too large. Max size: {settings.MAX_UPLOAD_SIZE} bytes")
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Generate file path
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{document_id}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        try:
            # Save file temporarily
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            logger.info(f"Saved file to {file_path}")
            
            # Ingest document (this will delete the file after processing)
            result = await self.ingestion_service.ingest_document(
                file_path=file_path,
                document_id=document_id,
                filename=file.filename
            )
            
            return {
                "success": True,
                "document_id": document_id,
                "filename": file.filename,
                "file_size": file_size,
                "total_chunks": result["total_chunks"],
                "status": "indexed"
            }
            
        except Exception as e:
            # Clean up file if something goes wrong
            if os.path.exists(file_path):
                self.file_processor.delete_file(file_path)
            logger.error(f"Error uploading document: {e}")
            raise
    
    def list_documents(self) -> List[Dict]:
        """
        List all documents from ChromaDB metadata
        
        Returns:
            List of documents
        """
        try:
            # Get all documents from ChromaDB collection
            collection = vector_repository.collection
            
            # Get unique document IDs from metadata
            all_data = collection.get()
            
            if not all_data or not all_data['metadatas']:
                return []
            
            # Extract unique documents
            documents = {}
            for metadata in all_data['metadatas']:
                doc_id = metadata.get('document_id')
                if doc_id and doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "filename": metadata.get('document_name', 'Unknown'),
                        "total_chunks": metadata.get('total_chunks', 0)
                    }
            
            return list(documents.values())
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete document from ChromaDB
        
        Args:
            document_id: Document ID to delete
        
        Returns:
            True if successful
        """
        try:
            vector_repository.delete_by_document_id(document_id)
            logger.info(f"Deleted document: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False


# Create global instance
document_service = DocumentService()
