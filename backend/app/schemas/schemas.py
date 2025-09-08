from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, Literal
from enum import Enum

class ItemType(str, Enum):
    BURGERS = "burgers"
    FRIES = "fries"
    DRINKS = "drinks"

class ActionType(str, Enum):
    PLACED = "placed"
    CANCELED = "canceled"
    MODIFIED = "modified"
    ERROR = "error"
    NONE = "none"

class OrderRequest(BaseModel):
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        description="User message for ordering or canceling"
    )
    
    @validator('message')
    def validate_message(cls, v):
        cleaned = v.strip()
        if not cleaned:
            raise ValueError('Message cannot be empty')
        return cleaned

class OrderResponse(BaseModel):
    success: bool = Field(..., description="Whether the action was successful")
    action: ActionType = Field(..., description="Type of action performed")
    order_id: Optional[int] = Field(None, description="Order ID for placed/canceled orders")
    items: Optional[Dict[str, int]] = Field(None, description="Items in the order")
    message: Optional[str] = Field(None, description="Human-readable message")
    totals: Dict[str, int] = Field(..., description="Current totals across all orders")
    orders: Dict[int, Dict[str, int]] = Field(..., description="All active orders")

class ParsedIntent(BaseModel):
    success: bool
    action: Literal["place_order", "cancel_order"]
    data: Dict
    confidence: Optional[float] = None
    raw_response: Optional[str] = None

class OrderItems(BaseModel):
    burgers: int = Field(0, ge=0, le=50)
    fries: int = Field(0, ge=0, le=50)  
    drinks: int = Field(0, ge=0, le=50)
    
    @validator('*', pre=True)
    def validate_quantities(cls, v):
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                v = 0
        return max(0, v) if isinstance(v, (int, float)) else 0
    
    def to_dict(self) -> Dict[str, int]:
        return {
            "burgers": self.burgers,
            "fries": self.fries,
            "drinks": self.drinks
        }
    
    def is_empty(self) -> bool:
        return self.burgers == 0 and self.fries == 0 and self.drinks == 0
    
    def total_items(self) -> int:
        return self.burgers + self.fries + self.drinks