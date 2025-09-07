from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import threading

@dataclass
class OrderInfo:
    id: int
    items: Dict[str, int]
    timestamp: datetime
    status: str = "active"

class OrderStore:
    
    def __init__(self):
        self._orders: Dict[int, OrderInfo] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()
    
    def add_order(self, items: Dict[str, int]) -> int:
        with self._lock:
            order_id = self._next_id
            self._orders[order_id] = OrderInfo(
                id=order_id,
                items=items.copy(),
                timestamp=datetime.now(),
                status="active"
            )
            self._next_id += 1
            return order_id
    
    def cancel_order(self, order_id: int) -> Optional[Dict[str, int]]:
        with self._lock:
            order_info = self._orders.get(order_id)
            if order_info and order_info.status == "active":
                order_info.status = "canceled"
                return order_info.items.copy()
            return None
    
    def get_order(self, order_id: int) -> Optional[OrderInfo]:
        with self._lock:
            return self._orders.get(order_id)
    
    def get_totals(self) -> Dict[str, int]:
        totals = {"burgers": 0, "fries": 0, "drinks": 0}
        
        with self._lock:
            for order_info in self._orders.values():
                if order_info.status == "active":
                    for item_type, quantity in order_info.items.items():
                        if item_type in totals:
                            totals[item_type] += quantity
        
        return totals
    
    def get_orders(self) -> Dict[int, Dict[str, int]]:
        with self._lock:
            return {
                order_id: order_info.items.copy()
                for order_id, order_info in self._orders.items()
                if order_info.status == "active"
            }
    
    def get_all_orders(self) -> Dict[int, OrderInfo]:
        with self._lock:
            return self._orders.copy()
    
    def get_order_history(self) -> List[OrderInfo]:
        with self._lock:
            return sorted(
                self._orders.values(),
                key=lambda x: x.timestamp,
                reverse=True
            )
    
    def get_stats(self) -> Dict:
        with self._lock:
            active_orders = [o for o in self._orders.values() if o.status == "active"]
            canceled_orders = [o for o in self._orders.values() if o.status == "canceled"]
            
            return {
                "total_orders": len(self._orders),
                "active_orders": len(active_orders),
                "canceled_orders": len(canceled_orders),
                "next_order_id": self._next_id
            }
    
    def clear_all(self) -> None:
        with self._lock:
            self._orders.clear()
            self._next_id = 1
    
    def has_order(self, order_id: int) -> bool:
        with self._lock:
            order_info = self._orders.get(order_id)
            return order_info is not None and order_info.status == "active"