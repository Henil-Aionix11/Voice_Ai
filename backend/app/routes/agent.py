"""
Agent configuration routes (in-memory storage)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.config.config_manager import config_manager
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])


class PromptUpdate(BaseModel):
    """Request model for updating agent prompt"""
    prompt: str


@router.get("/prompt")
async def get_prompt():
    """
    Get current agent system prompt
    """
    try:
        prompt = config_manager.get_prompt()
        return {
            "success": True,
            "data": {
                "prompt": prompt
            }
        }
    except Exception as e:
        logger.error(f"Error getting prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/prompt")
async def update_prompt(update: PromptUpdate):
    """
    Update agent system prompt (in-memory only)
    
    Note: Changes are NOT persisted. Restarting the app will reset to default.
    """
    try:
        if not update.prompt or len(update.prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        new_prompt = config_manager.update_prompt(update.prompt)
        
        return {
            "success": True,
            "data": {
                "prompt": new_prompt,
                "message": "Prompt updated successfully (in-memory only)"
            }
        }
    except Exception as e:
        logger.error(f"Error updating prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/prompt/reset")
async def reset_prompt():
    """
    Reset prompt to default
    """
    try:
        default_prompt = config_manager.reset_prompt()
        return {
            "success": True,
            "data": {
                "prompt": default_prompt,
                "message": "Prompt reset to default"
            }
        }
    except Exception as e:
        logger.error(f"Error resetting prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
