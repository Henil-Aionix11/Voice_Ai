"""
Document management routes (simplified - no database!)
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.document_service import document_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(files: List[UploadFile] = File(...)):
    """
    Upload multiple documents for ingestion into the RAG system
    
    Accepts: PDF, TXT files
    Processes each file based on its type automatically
    """
    try:
        results = await document_service.upload_documents(files)
        return {
            "success": True,
            "data": results,
            "total_uploaded": len(results["successful"]),
            "total_failed": len(results["failed"])
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/")
async def list_documents():
    """
    Get list of all uploaded documents from ChromaDB
    """
    try:
        documents = document_service.list_documents()
        return {
            "success": True,
            "data": documents
        }
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document and its associated chunks from ChromaDB
    """
    try:
        success = document_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "success": True,
            "message": "Document deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
