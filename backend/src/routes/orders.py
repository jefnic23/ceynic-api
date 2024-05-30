from fastapi import APIRouter

from backend.src.dependencies import ORDERS_SERVICE_DEPENDENCY
from backend.src.models.schemas.create_order_request import CreateOrderRequest

router = APIRouter()


@router.post("/orders")
async def send_contact_email(
    create_order_request: CreateOrderRequest, orders: ORDERS_SERVICE_DEPENDENCY
) -> str:
    order_id = await orders.create_order(product_id=create_order_request.product_id)

    return order_id
