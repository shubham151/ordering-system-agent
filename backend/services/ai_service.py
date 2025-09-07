import logging
from typing import Dict, Any
from config import Config
from services.ai_providers import OpenAIProvider, GeminiProvider

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, provider: str = None):
        self.provider_name = provider or Config.AI_PROVIDER
        
        if self.provider_name == "openai":
            self.provider = OpenAIProvider()
        elif self.provider_name == "gemini":
            self.provider = GeminiProvider()
        else:
            raise ValueError(f"Unsupported provider: {self.provider_name}")
        
        logger.info(f"AI Service initialized with {self.provider_name} provider")
    
    def parse_user_intent(self, message: str) -> Dict[str, Any]:
        if not message or not message.strip():
            return {"success": False, "error": "Empty message"}
        
        return self.provider.parse_intent(message.strip())