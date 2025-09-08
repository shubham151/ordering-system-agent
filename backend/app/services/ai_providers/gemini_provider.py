import json
import logging
from typing import Dict, Any
from app.core.config import Config
from .base import AIProvider, get_system_prompt, get_function_definitions

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self):
        try:
            import google.generativeai as genai
            if not Config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not found in config")
            
            genai.configure(api_key=Config.GEMINI_API_KEY)
            tools = self._convert_functions_to_tools(get_function_definitions())
            self.model = genai.GenerativeModel(
                Config.GEMINI_MODEL,
                tools=tools
            )
            
        except ImportError:
            raise ImportError("google-generativeai package not installed")
    
    def parse_intent(self, message: str) -> Dict[str, Any]:
        try:
            response = self.model.generate_content(
                [get_system_prompt(), message],
                tool_config={'function_calling_config': 'AUTO'}
            )
            
            # Check if model called a function
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        function_call = part.function_call
                        return {
                            "success": True,
                            "action": function_call.name,
                            "data": dict(function_call.args),
                            "raw_response": str(response)
                        }
            
            return {
                "success": False,
                "error": "No function call detected",
                "raw_response": response.text if response.text else "No response"
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return {"success": False, "error": f"API error: {str(e)}"}
    
    def _convert_functions_to_tools(self, openai_functions: list) -> list:
        import google.generativeai as genai
        
        tools = []
        for func in openai_functions:
            tool = genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name=func["name"],
                        description=func["description"],
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                prop_name: genai.protos.Schema(
                                    type=self._get_gemini_type(prop_info["type"]),
                                    description=prop_info["description"]
                                )
                                for prop_name, prop_info in func["parameters"]["properties"].items()
                            },
                            required=func["parameters"].get("required", [])
                        )
                    )
                ]
            )
            tools.append(tool)
        
        return tools
    
    def _get_gemini_type(self, openai_type: str):
        """Convert OpenAI parameter types to Gemini types"""
        import google.generativeai as genai
        
        type_mapping = {
            "string": genai.protos.Type.STRING,
            "integer": genai.protos.Type.INTEGER,
            "number": genai.protos.Type.NUMBER,
            "boolean": genai.protos.Type.BOOLEAN,
            "array": genai.protos.Type.ARRAY,
            "object": genai.protos.Type.OBJECT
        }
        return type_mapping.get(openai_type, genai.protos.Type.STRING)