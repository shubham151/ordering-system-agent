from fastapi import APIRouter, Depends
from schema import OrderRequest, OrderResponse
from dependencies import OrderServiceDep, OrderStoreDep
from services.order_service import OrderService
from models import OrderStore
from utils.response_utils import success_response, error_response
from utils.exceptions import handle_exceptions
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Orders"])

# ---------- Order Processing ----------
@router.post("/process", response_model=OrderResponse)
@handle_exceptions
async def process_order(
    request: OrderRequest,
    order_service: OrderServiceDep
) -> OrderResponse:
    return await order_service.process_user_message(request.message)

# ---------- Order Management ----------
@router.get("/orders")
@handle_exceptions
async def get_orders(order_service: OrderServiceDep):
    return await order_service.get_all_orders_with_stats()

@router.get("/orders/{order_id}")
@handle_exceptions
async def get_order(order_id: int, order_service: OrderServiceDep):
    return await order_service.get_order_details(order_id)

@router.delete("/orders/{order_id}")
@handle_exceptions
async def cancel_order(order_id: int, order_service: OrderServiceDep):
    return await order_service.cancel_order_by_id(order_id)

# ---------- Statistics ----------
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