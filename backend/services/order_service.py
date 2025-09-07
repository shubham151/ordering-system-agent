import logging
from typing import Dict, Any
from models import OrderStore
from schema import OrderResponse, OrderItems, ActionType

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, order_store: OrderStore):
        self.order_store = order_store
    
    def execute_action(self, parsed_intent: Dict[str, Any]) -> OrderResponse:
        action = parsed_intent.get("action")
        data = parsed_intent.get("data", {})
        
        if action == "place_order":
            return self.place_order(data)
        elif action == "cancel_order":
            return self.cancel_order(data.get("order_id"))
        else:
            logger.warning(f"Unknown action: {action}")
            return self._create_error_response("Unknown action requested")
    
    def place_order(self, order_data: Dict[str, Any]) -> OrderResponse:
        try:
            # Validate and clean order data
            order_items = OrderItems(**order_data)
            
            if order_items.is_empty():
                return self._create_error_response(
                    "Please specify at least one item to order"
                )
            
            # Add order to store
            items_dict = order_items.to_dict()
            order_id = self.order_store.add_order(items_dict)
            
            # Create success message
            message = self._format_order_message(order_items, order_id)
            
            logger.info(f"Order {order_id} placed: {items_dict}")
            
            return OrderResponse(
                success=True,
                action=ActionType.PLACED,
                order_id=order_id,
                items=items_dict,
                message=message,
                totals=self.order_store.get_totals(),
                orders=self.order_store.get_orders(),
            )
            
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return self._create_error_response("Failed to place order")
    
    def cancel_order(self, order_id: int) -> OrderResponse:
        try:
            if order_id is None:
                return self._create_error_response(
                    "Please specify an order number to cancel"
                )
            
            canceled_items = self.order_store.cancel_order(order_id)
            
            if canceled_items:
                message = f"Order #{order_id} has been canceled"
                logger.info(f"Order {order_id} canceled: {canceled_items}")
                
                return OrderResponse(
                    success=True,
                    action=ActionType.CANCELED,
                    order_id=order_id,
                    items=canceled_items,
                    message=message,
                    totals=self.order_store.get_totals(),
                    orders=self.order_store.get_orders(),
                )
            else:
                return self._create_error_response(
                    f"Order #{order_id} not found or already canceled"
                )
                
        except Exception as e:
            logger.error(f"Error canceling order {order_id}: {str(e)}")
            return self._create_error_response("Failed to cancel order")
    
    def _create_error_response(self, message: str) -> OrderResponse:
        return OrderResponse(
            success=False,
            action=ActionType.ERROR,
            message=message,
            totals=self.order_store.get_totals(),
            orders=self.order_store.get_orders(),
        )
    
    def _format_order_message(self, order_items: OrderItems, order_id: int) -> str:
        items = []
        
        if order_items.burgers > 0:
            items.append(f"{order_items.burgers} burger{'s' if order_items.burgers != 1 else ''}")
        
        if order_items.fries > 0:
            items.append(f"{order_items.fries} order{'s' if order_items.fries != 1 else ''} of fries")
        
        if order_items.drinks > 0:
            items.append(f"{order_items.drinks} drink{'s' if order_items.drinks != 1 else ''}")
        
        if len(items) == 1:
            items_text = items[0]
        elif len(items) == 2:
            items_text = f"{items[0]} and {items[1]}"
        else:
            items_text = f"{', '.join(items[:-1])}, and {items[-1]}"
        
        return f"Order #{order_id} placed: {items_text}"

def validate_order_items(data: Dict[str, Any]) -> tuple[bool, OrderItems, str]:
    try:
        order_items = OrderItems(**data)
        if order_items.is_empty():
            return False, order_items, "Please specify at least one item to order"
        return True, order_items, ""
    except Exception as e:
        return False, OrderItems(), f"Invalid order data: {str(e)}"

def validate_order_id(order_id: Any) -> tuple[bool, int, str]:
    try:
        if order_id is None:
            return False, 0, "Please specify an order number to cancel"
        
        order_id_int = int(order_id)
        if order_id_int <= 0:
            return False, 0, "Order number must be positive"
        
        return True, order_id_int, ""
    except (ValueError, TypeError):
        return False, 0, "Invalid order number format"