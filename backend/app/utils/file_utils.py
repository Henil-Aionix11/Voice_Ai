"""
File processing utilities
"""
import os
from typing import Optional
from langchain_community.document_loaders import PyMuPDFLoader
from app.config.constants import SUPPORTED_FILE_TYPES
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FileProcessor:
    """File processing utilities for document extraction"""
    
    @staticmethod
    def is_supported_file(filename: str) -> bool:
        """Check if file type is supported"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in SUPPORTED_FILE_TYPES
    
    @staticmethod
    async def extract_text(file_path: str) -> str:
        """
        Extract text from PDF or TXT files
        
        Args:
            file_path: Path to the file
        
        Returns:
            Extracted text content
        
        Raises:
            ValueError: If file type is not supported
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        logger.info(f"Extracting text from {file_path} (type: {file_extension})")
        
        if file_extension == '.pdf':
            # Use LangChain's PyMuPDF loader for PDF extraction
            loader = PyMuPDFLoader(file_path)
            documents = loader.load()
            text = "\n\n".join([doc.page_content for doc in documents])
            logger.info(f"Extracted {len(text)} characters from PDF")
            
        elif file_extension == '.txt':
            # Simple text file reading
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Extracted {len(text)} characters from TXT")
            
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        return text
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Safely delete a file
        
        Args:
            file_path: Path to the file to delete
        
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
