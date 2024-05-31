from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.src.dependencies import ORDERS_SERVICE_DEPENDENCY
from backend.src.models.schemas.paypal import CapturePaymentResponse, CreateOrderRequest

router = APIRouter()


@router.post("/orders")
async def create_order(
    create_order_request: CreateOrderRequest, orders: ORDERS_SERVICE_DEPENDENCY
) -> JSONResponse:
    order_id = await orders.create_order(product_id=create_order_request.product_id)

    return JSONResponse({"order_id": order_id})


@router.post("/orders/{order_id}")
async def capture_payment(
    order_id: str,
    create_order_request: CreateOrderRequest,
    orders: ORDERS_SERVICE_DEPENDENCY,
) -> CapturePaymentResponse:
    response = await orders.capture_payment(
        order_id=order_id, product_id=create_order_request.product_id
    )

    return response
