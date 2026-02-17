"""
LiveKit Agent service with OpenAI Realtime API integration
"""
from typing import Dict
import os
import json
from livekit.agents import AutoSubscribe, JobContext, llm, Agent, AgentSession
from livekit.plugins import openai
from app.services.retrieval_service import retrieval_service
from app.config.config_manager import config_manager
from app.config.constants import (
    REALTIME_MODEL,
    REALTIME_VOICE,
    REALTIME_TEMPERATURE,
    RAG_TOP_K
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LiveKitAgentService:
    """
    LiveKit Voice Agent using OpenAI Realtime API
    
    Pipeline:
    Audio Input -> OpenAI Realtime (STT) -> LLM (with RAG) -> OpenAI Realtime (TTS) -> Audio Output
    """
    
    def __init__(self):
        self.retrieval_service = retrieval_service
        self.config_manager = config_manager
        self._rag_context_prefix = "[RAG_CONTEXT]"

    async def _publish_data(self, ctx: JobContext, payload: Dict):
        """Publish JSON payload to room participants."""
        try:
            data = json.dumps(payload).encode("utf-8")
            await ctx.room.local_participant.publish_data(data, reliable=True)
        except Exception as e:
            logger.error(f"Failed to publish data: {e}")
    
    async def entrypoint(self, ctx: JobContext):
        """
        Main entrypoint for LiveKit agent
        
        Args:
            ctx: LiveKit JobContext
        """
        logger.info("LiveKit agent starting...")
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OPENAI_API_KEY is not set in this process environment")
        else:
            logger.info("OPENAI_API_KEY is set for agent process")
        
        # Connect to LiveKit room
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        logger.info(f"Connected to room: {ctx.room.name}")
        
        # Get current system prompt from config manager (in-memory)
        system_prompt = self.config_manager.get_prompt()
        logger.info(f"Using system prompt ({len(system_prompt)} characters)")
        
        # Initialize OpenAI Realtime model for voice
        realtime_model = openai.realtime.RealtimeModel(
            model=REALTIME_MODEL,
            voice=REALTIME_VOICE,
            temperature=REALTIME_TEMPERATURE,
            instructions=system_prompt
        )
        
        logger.info(f"Initialized OpenAI Realtime model: {REALTIME_MODEL}")
        
        # Create initial agent with system instructions
        initial_agent = Agent(
            instructions=system_prompt
        )
        
        # Create AgentSession with the realtime model
        session = AgentSession(
            llm=realtime_model,
            agent=initial_agent
        )
        
        # Handle transcription events for RAG
        @session.on("user_input_transcribed")
        async def on_user_input_transcribed(event):
            """
            Called when user speech is transcribed
            
            Args:
                event: UserInputTranscribedEvent containing transcript and metadata
            """
            # Only process final transcriptions
            if not event.is_final:
                return
                
            user_text = event.transcript
            logger.info(f"User said: {user_text}")

            # Publish user transcript
            await self._publish_data(ctx, {
                "type": "user_transcript",
                "text": user_text
            })
            
            # Retrieve relevant context from documents
            context_chunks = await self.retrieval_service.retrieve_context(
                query=user_text,
                top_k=RAG_TOP_K
            )
            
            # Build per-turn RAG context message
            if context_chunks:
                context_str = "\n\n".join([
                    f"[Source: {chunk['document_name']}]\n{chunk['text']}"
                    for chunk in context_chunks
                ])
                rag_message = (
                    f"{self._rag_context_prefix}\n"
                    f"RELEVANT CONTEXT FROM DOCUMENTS:\n{context_str}\n\n"
                    f"USER QUESTION: {user_text}\n"
                    f"Use the context above to answer the question. "
                    f"If the context doesn't contain relevant information, say so clearly."
                )
                logger.info(f"Retrieved {len(context_chunks)} relevant chunks")

                # Publish RAG sources for frontend panel
                await self._publish_data(ctx, {
                    "type": "rag_sources",
                    "sources": [
                        {
                            "document_name": chunk["document_name"],
                            "text": chunk["text"],
                            "distance": chunk.get("distance")
                        }
                        for chunk in context_chunks
                    ]
                })
                
                # Add RAG context to the session
                session.send_message(llm.ChatMessage(
                    role="user",
                    content=rag_message
                ))
            else:
                logger.info("No relevant documents found")

        @session.on("speech_created")
        async def on_speech_created(event):
            """Called when agent speech is created."""
            # The speech_created event is emitted when agent starts speaking
            # We'll log this but the actual speech text comes from the TTS stream
            logger.info("Agent is generating speech")
            

        @session.on("error")
        async def on_session_error(err: Exception):
            logger.error(f"Agent session error: {err}")
        
        # Start the session
        logger.info("Starting agent session...")
        await session.start(ctx.room)


# Create service function for LiveKit worker
async def livekit_agent_entrypoint(ctx: JobContext):
    """
    Entrypoint function for LiveKit worker
    
    This is the function that LiveKit will call when a new room is created
    """
    agent_service = LiveKitAgentService()
    await agent_service.entrypoint(ctx)
