"""
LiveKit routes for room management and token generation
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from livekit import api
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/livekit", tags=["livekit"])


class TokenRequest(BaseModel):
    """Request model for LiveKit token generation"""
    room_name: str
    participant_name: str


@router.post("/token")
async def create_token(request: TokenRequest):
    """
    Generate a LiveKit access token for a participant
    
    Args:
        room_name: Name of the room to join
        participant_name: Name of the participant
    
    Returns:
        Access token for LiveKit room
    """
    try:
        # Create token with API credentials
        token = api.AccessToken(
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET
        )
        
        # Set token parameters
        token.with_identity(request.participant_name)
        token.with_name(request.participant_name)
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room=request.room_name,
                can_publish=True,
                can_subscribe=True
            )
        )
        
        # Generate JWT token
        jwt_token = token.to_jwt()
        
        logger.info(f"Generated token for {request.participant_name} in room {request.room_name}")
        
        return {
            "success": True,
            "data": {
                "token": jwt_token,
                "url": settings.LIVEKIT_URL,
                "room_name": request.room_name,
                "participant_name": request.participant_name
            }
        }
    except Exception as e:
        logger.error(f"Error generating LiveKit token: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate token")


@router.get("/rooms")
async def list_rooms():
    """
    List all active LiveKit rooms
    
    Note: This requires LiveKit Cloud or a local LiveKit server
    """
    try:
        # This would require the LiveKit SDK to query rooms
        # For now, return a simple response
        return {
            "success": True,
            "data": {
                "rooms": [],
                "message": "Room listing requires LiveKit server API access"
            }
        }
    except Exception as e:
        logger.error(f"Error listing rooms: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
