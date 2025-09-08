from fastapi import APIRouter, Depends
from app.schemas.schemas import OrderRequest, OrderResponse
from app.core.dependencies import OrderServiceDep, OrderStoreDep
from app.services.order_service import OrderService
from app.models.db_models import OrderStore
from app.utils.response_utils import success_response, error_response
from app.utils.exception_utils import handle_exceptions

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Orders"])

@router.post("/process", response_model=OrderResponse)
@handle_exceptions
def process_order(request: OrderRequest, order_service: OrderServiceDep) -> OrderResponse:
    return order_service.process_order_request(request) 

@router.get("/orders")
@handle_exceptions
def get_orders(order_service: OrderServiceDep):
    return order_service.get_current_orders()

@router.get("/orders/{order_id}")
@handle_exceptions
async def get_order(order_id: int, order_service: OrderServiceDep):
    return await order_service.get_order_details(order_id)

@router.delete("/orders/{order_id}")
@handle_exceptions
async def cancel_order(order_id: int, order_service: OrderServiceDep):
    return await order_service.cancel_order_by_id(order_id)

@router.get("/orders/stats")
@handle_exceptions
async def get_stats(order_service: OrderServiceDep):
    return await order_service.get_comprehensive_stats()

@router.get("/orders/history")
@handle_exceptions
async def get_history(
    order_service: OrderServiceDep,
    limit: int = 50
):
    return await order_service.get_order_history(limit)