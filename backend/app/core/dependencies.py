from fastapi import Request, Depends, HTTPException
from app.services.order_service import OrderService
from app.services.ai_service import AIService
from app.models.db_models import OrderStore
from typing import Annotated

# ---------- Core Dependencies ----------

def get_order_store(request: Request) -> OrderStore:
    return request.app.state.order_store

def get_ai_service(request: Request) -> AIService:
    return request.app.state.ai_service

def get_order_service(request: Request) -> OrderService:
    return request.app.state.order_service

OrderStoreDep = Annotated[OrderStore, Depends(get_order_store)]
AIServiceDep = Annotated[AIService, Depends(get_ai_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]

# ---------- Composite Dependencies ----------

def get_all_services(request: Request) -> tuple[OrderStore, AIService, OrderService]:
    return (
        request.app.state.order_store,
        request.app.state.ai_service,
        request.app.state.order_service
    )

AllServicesDep = Annotated[
    tuple[OrderStore, AIService, OrderService], 
    Depends(get_all_services)
]

# ---------- Validation Dependencies ----------

def validate_order_id(order_id: int) -> int:
    if order_id <= 0:
        raise HTTPException(status_code=400, detail="Order ID must be positive")
    return order_id

ValidOrderIdDep = Annotated[int, Depends(validate_order_id)]