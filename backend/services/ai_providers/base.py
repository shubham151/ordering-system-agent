from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    @abstractmethod
    def parse_intent(self, message: str) -> Dict[str, Any]:
        pass

def get_system_prompt() -> str:
    return """You are a drive-thru ordering assistant. Your job is to:

1. PLACE ORDERS: Parse requests for burgers, fries, and drinks with specific quantities
2. CANCEL ORDERS: Process cancellation requests with order numbers

Key rules:
- If no quantity is specified, assume 1
- Extract ALL mentioned items and quantities
- Look for phrases like "each", "both", "all of us" to multiply quantities
- Order numbers can be mentioned as "order 5", "#5", "order number 5", etc.
- Only respond with the specified function calls

Examples:
- "I want 2 burgers and 3 fries" → place_order(burgers=2, fries=3, drinks=0)
- "My friend and I each want a drink" → place_order(burgers=0, fries=0, drinks=2)
- "Cancel order 5" → cancel_order(order_id=5)
- "Please cancel my order #3" → cancel_order(order_id=3)"""

def get_function_definitions() -> list:
    return [
        {
            "name": "place_order",
            "description": "Place a food order with specified quantities",
            "parameters": {
                "type": "object",
                "properties": {
                    "burgers": {"type": "integer", "description": "Number of burgers", "default": 0},
                    "fries": {"type": "integer", "description": "Number of fries", "default": 0},
                    "drinks": {"type": "integer", "description": "Number of drinks", "default": 0},
                },
                "required": []
            },
        },
        {
            "name": "cancel_order",
            "description": "Cancel an existing order by order number",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "The order number to cancel"},
                },
                "required": ["order_id"],
            },
        },
    ]