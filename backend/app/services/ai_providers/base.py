from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    @abstractmethod
    def parse_intent(self, message: str) -> Dict[str, Any]:
        pass

def get_system_prompt() -> str:
    return """You are a drive-thru ordering assistant. Your job is to:

1. PLACE ORDERS: Parse requests for burgers, fries, and drinks with specific quantities
2. MODIFY ORDERS: Update existing orders by adding, removing, or changing items
3. CANCEL ORDERS: Process cancellation requests with order numbers

Key rules:
- If no quantity is specified, assume 1
- Extract ALL mentioned items and quantities
- Look for phrases like "each", "both", "all of us" to multiply quantities
- Order numbers can be mentioned as "order 5", "#5", "order number 5", etc.
- For modifications: "add", "remove", "change", "update", "modify" indicate order changes
- For modifications: always specify what to add/remove and the order ID
- Only respond with the specified function calls

PLACE ORDER Examples:
- "I want 2 burgers and 3 fries" → place_order(burgers=2, fries=3, drinks=0)
- "My friend and I each want a drink" → place_order(burgers=0, fries=0, drinks=2)
- "Can I get one of everything" → place_order(burgers=1, fries=1, drinks=1)

MODIFY ORDER Examples:
- "Update my order 1 with 2 more burgers and no fries" → modify_order(order_id=1, add_burgers=2, remove_fries=999)
- "Add 3 drinks to order 2" → modify_order(order_id=2, add_drinks=3)
- "Remove all burgers from order 3" → modify_order(order_id=3, remove_burgers=999)
- "Change order 1 to have 5 burgers instead" → modify_order(order_id=1, set_burgers=5)

CANCEL ORDER Examples:
- "Cancel order 5" → cancel_order(order_id=5)
- "Please cancel my order #3" → cancel_order(order_id=3)

MODIFICATION RULES:
- add_X: Add X items to existing quantity
- remove_X: Remove X items (use 999 to remove all)
- set_X: Set total quantity to X (replaces current amount)
- Always include order_id for modifications"""

def get_function_definitions() -> list:
    return [
        {
            "name": "place_order",
            "description": "Place a new food order with specified quantities",
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
            "name": "modify_order",
            "description": "Modify an existing order by adding, removing, or setting item quantities",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "The order number to modify"},
                    "add_burgers": {"type": "integer", "description": "Number of burgers to add", "default": 0},
                    "add_fries": {"type": "integer", "description": "Number of fries to add", "default": 0},
                    "add_drinks": {"type": "integer", "description": "Number of drinks to add", "default": 0},
                    "remove_burgers": {"type": "integer", "description": "Number of burgers to remove (999=all)", "default": 0},
                    "remove_fries": {"type": "integer", "description": "Number of fries to remove (999=all)", "default": 0},
                    "remove_drinks": {"type": "integer", "description": "Number of drinks to remove (999=all)", "default": 0},
                    "set_burgers": {"type": "integer", "description": "Set total burgers to this amount", "default": -1},
                    "set_fries": {"type": "integer", "description": "Set total fries to this amount", "default": -1},
                    "set_drinks": {"type": "integer", "description": "Set total drinks to this amount", "default": -1},
                },
                "required": ["order_id"]
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