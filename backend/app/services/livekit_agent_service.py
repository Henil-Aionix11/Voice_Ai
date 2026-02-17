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
            temperature=REALTIME_TEMPERATURE
        )
        
        logger.info(f"Initialized OpenAI Realtime model: {REALTIME_MODEL}")
        
        # Create AgentSession with the realtime model
        # For Realtime models, we pass them as the llm parameter
        session = AgentSession(
            llm=realtime_model
        )
        
        # Handle transcription events for RAG
        @session.on("user_input_transcribed")
        def on_user_input_transcribed(event):
            """
            Called when user speech is transcribed
            
            Args:
                event: UserInputTranscribedEvent containing transcript and metadata
            """
            async def handle_transcription():
                # Only process final transcriptions
                if not event.is_final:
                    return
                    
                user_text = event.transcript
                
                # Skip empty or whitespace-only transcripts
                if not user_text or not user_text.strip():
                    return
                    
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
                    
                    # NOTE: For Realtime API, context injection works differently
                    # The model uses the system instructions instead of per-turn context injection
                    # RAG context is displayed in the frontend panel for user reference
                else:
                    logger.info("No relevant documents found")
            
            # Use asyncio.create_task to run the async handler
            import asyncio
            asyncio.create_task(handle_transcription())

        @session.on("speech_created")
        def on_speech_created(event):
            """Called when agent speech is created."""
            # The speech_created event is emitted when agent starts speaking
            # We'll log this but the actual speech text comes from the TTS stream
            logger.info("Agent is generating speech")
            

        @session.on("error")
        def on_session_error(err: Exception):
            logger.error(f"Agent session error: {err}")
        
        # Create the agent with system instructions
        agent = Agent(
            instructions=system_prompt
        )
        
        # Start the session with both room and agent
        logger.info("Starting agent session...")
        await session.start(room=ctx.room, agent=agent)


# Create service function for LiveKit worker
async def livekit_agent_entrypoint(ctx: JobContext):
    """
    Entrypoint function for LiveKit worker
    
    This is the function that LiveKit will call when a new room is created
    """
    agent_service = LiveKitAgentService()
    await agent_service.entrypoint(ctx)
