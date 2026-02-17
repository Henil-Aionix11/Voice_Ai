"""
LLM service for generating responses with RAG
"""
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from app.config.settings import settings
from app.config.constants import LLM_MODEL
from app.config.prompt import RAG_SYSTEM_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    """Service for LLM-powered responses with RAG integration"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = LLM_MODEL
    
    async def generate_response(
        self,
        user_query: str,
        context_chunks: List[Dict],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate response using GPT-4o-mini with RAG context
        
        Args:
            user_query: User's question
            context_chunks: Retrieved chunks from RAG
            system_prompt: Optional custom system prompt
        
        Returns:
            Generated response text
        """
        logger.info(f"Generating response for query: {user_query[:100]}...")
        
        # Use provided prompt or default
        prompt = system_prompt or RAG_SYSTEM_PROMPT
        
        # Build context string from retrieved chunks
        if context_chunks:
            context_str = "\n\n".join([
                f"[Document: {chunk['document_name']}]\n{chunk['text']}"
                for chunk in context_chunks
            ])
            
            user_message = f"""Context from uploaded documents:

{context_str}

User question: {user_query}

Please answer the question based on the context above. If the context doesn't contain relevant information, clearly state that you cannot answer based on the available documents."""
        else:
            user_message = f"{user_query}\n\nNote: No relevant documents were found in the knowledge base."
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Generated response ({len(answer)} characters)")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise


# Create global instance
llm_service = LLMService()
