"""
Chat/Query routes for testing RAG (text-based)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.retrieval_service import retrieval_service
from app.services.llm_service import llm_service
from app.config.config_manager import config_manager
from app.config.constants import RAG_TOP_K
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


class QueryRequest(BaseModel):
    """Request model for text query"""
    question: str


class QueryResponse(BaseModel):
    """Response model for query"""
    success: bool
    answer: str
    sources: List[Dict]
    chunks_used: int


@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Test RAG pipeline with text query (for testing only)
    
    This endpoint is for testing the RAG system without voice.
    The actual voice flow uses LiveKit + OpenAI Realtime API.
    
    Args:
        question: User question
    
    Returns:
        Answer generated from RAG with sources
    """
    try:
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"RAG Query: {request.question}")
        
        # 1. Retrieve relevant context from ChromaDB (using default TOP_K from constants)
        context_chunks = await retrieval_service.retrieve_context(
            query=request.question,
            top_k=RAG_TOP_K
        )
        
        if not context_chunks:
            logger.warning("No relevant documents found")
            return QueryResponse(
                success=True,
                answer="I don't have any relevant information in my knowledge base to answer this question.",
                sources=[],
                chunks_used=0
            )
        
        # 2. Get current system prompt
        system_prompt = config_manager.get_prompt()
        
        # 3. Generate answer using LLM with RAG context
        answer = await llm_service.generate_response(
            user_query=request.question,
            context_chunks=context_chunks,
            system_prompt=system_prompt
        )
        
        # 4. Format sources
        sources = [
            {
                "document_name": chunk.get("document_name", "Unknown"),
                "text": chunk.get("text", ""),
                "similarity": chunk.get("similarity", 0.0)
            }
            for chunk in context_chunks
        ]
        
        logger.info(f"Generated answer using {len(context_chunks)} chunks")
        
        return QueryResponse(
            success=True,
            answer=answer,
            sources=sources,
            chunks_used=len(context_chunks)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/query/simple")
async def simple_query(request: QueryRequest):
    """
    Simplified query endpoint (returns plain JSON)
    """
    try:
        result = await query_rag(request)
        return {
            "question": request.question,
            "answer": result.answer,
            "sources_count": result.chunks_used,
            "sources": result.sources
        }
    except Exception as e:
        logger.error(f"Error in simple query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
