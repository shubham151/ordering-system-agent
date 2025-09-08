import json
import logging
from typing import Dict, Any
from config import Config
from .base import AIProvider, get_system_prompt, get_function_definitions

logger = logging.getLogger(__name__)

class OpenAIProvider(AIProvider):
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    def parse_intent(self, message: str) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": message}
                ],
                functions=get_function_definitions(),
                function_call="auto",
                timeout=Config.AI_REQUEST_TIMEOUT
            )
            
            choice = response.choices[0].message
            if choice.function_call:
                return {
                    "success": True,
                    "action": choice.function_call.name,
                    "data": json.loads(choice.function_call.arguments),
                    "raw_response": str(response)
                }
            else:
                return {
                    "success": False,
                    "error": "No function call detected",
                    "raw_response": choice.content
                }
                
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return {"success": False, "error": f"API error: {str(e)}"}