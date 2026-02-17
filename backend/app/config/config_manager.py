"""
In-memory configuration manager for agent prompts
No database needed - perfect for demo!
"""
from app.config.prompt import AGENT_SYSTEM_PROMPT
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ConfigManager:
    """In-memory configuration manager"""
    
    def __init__(self):
        # Start with default prompt from prompt.py
        self._current_prompt = AGENT_SYSTEM_PROMPT
        logger.info("Initialized ConfigManager with default prompt")
    
    def get_prompt(self) -> str:
        """Get current system prompt"""
        return self._current_prompt
    
    def update_prompt(self, new_prompt: str) -> str:
        """
        Update the system prompt (in-memory only)
        
        Args:
            new_prompt: New system prompt text
        
        Returns:
            Updated prompt
        """
        self._current_prompt = new_prompt
        logger.info(f"Updated system prompt ({len(new_prompt)} characters)")
        return self._current_prompt
    
    def reset_prompt(self) -> str:
        """Reset to default prompt"""
        self._current_prompt = AGENT_SYSTEM_PROMPT
        logger.info("Reset system prompt to default")
        return self._current_prompt


# Global singleton instance
config_manager = ConfigManager()
