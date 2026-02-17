"""
Text chunking utilities for RAG
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

from typing import List, Dict
from app.config.constants import CHUNK_SIZE, CHUNK_OVERLAP


class ChunkingStrategy:
    """
    Text chunking using RecursiveCharacterTextSplitter
    
    Configuration:
    - chunk_size: 1000 characters (~200 words)
    - chunk_overlap: 200 characters (20% overlap)
    - separators: paragraph, sentence, and word boundaries
    """
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
    
    def chunk_text(self, text: str, metadata: dict) -> List[Dict]:
        """
        Split text into chunks with metadata
        
        Args:
            text: The text to chunk
            metadata: Metadata to attach to each chunk (document_id, document_name, etc.)
        
        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        chunks = self.text_splitter.split_text(text)
        
        return [
            {
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": idx,
                    "total_chunks": len(chunks)
                }
            }
            for idx, chunk in enumerate(chunks)
        ]
