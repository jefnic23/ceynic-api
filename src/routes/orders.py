from fastapi import APIRouter, HTTPException

from src.dependencies import CURRENT_USER_DEPENDENCY, ORDERS_SERVICE_DEPENDENCY, PRODUCTS_SERVICE_DEPENDENCY, STOREFRONT_ID_DEPENDENCY
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.create_order_request import CreateOrderRequest
from src.schemas.order import OrdersOut
from src.schemas.paypal.authorize_payment_response import AuthorizePaymentResponse
from src.schemas.paypal.capture_payment_response import CapturePaymentResponse
from src.schemas.paypal.order_details import OrderDetails
from src.schemas.paypal.payments import Authorization

router = APIRouter()


@router.get("/orders")
async def get_orders(
    current_user: CURRENT_USER_DEPENDENCY,
    orders_service: ORDERS_SERVICE_DEPENDENCY
) -> list[OrdersOut]:
    orders = await orders_service.get_orders(current_user.storefront_id)
    return orders


@router.get("/orders/{order_id:str}")
async def get_order(
    order_id: str,
    current_user: CURRENT_USER_DEPENDENCY,
    orders_service: ORDERS_SERVICE_DEPENDENCY
) -> OrderDetails:
    order = await orders_service.get_order(storefront_id=current_user.storefront_id, order_id=order_id)
    return order


@router.post("/orders")
async def create_order(
    create_order_request: CreateOrderRequest,
    storefront_id: STOREFRONT_ID_DEPENDENCY, 
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    orders_service: ORDERS_SERVICE_DEPENDENCY
) -> CreateOrderOut:
    products = await products_service.get_for_order(
        storefront_id=storefront_id,
        product_ids=create_order_request.product_ids
    )
    if len(products) == 0:
        raise HTTPException(status_code=404, detail="Product(s) not found") 
    return await orders_service.create_order(storefront_id=storefront_id, products=products)


@router.post("/orders/{order_id:str}/authorize")
async def authorize_payment(
    order_id: str,
    create_order_request: CreateOrderRequest,
    orders_service: ORDERS_SERVICE_DEPENDENCY,
    storefront_id: STOREFRONT_ID_DEPENDENCY
) -> AuthorizePaymentResponse:
    response = await orders_service.authorize_payment(
        storefront_id=storefront_id,
        order_id=order_id, 
        product_ids=create_order_request.product_ids,
    )
    return response

@router.post("/orders/{order_id:str}/void")
async def void_authorized_payment(
    order_id: str,
    orders_service: ORDERS_SERVICE_DEPENDENCY,
    storefront_id: STOREFRONT_ID_DEPENDENCY
) -> Authorization:
    response = await orders_service.void_payment(
        storefront_id=storefront_id,
        order_id=order_id,
    )
    return response


@router.post("/orders/{order_id:str}/capture")
async def capture_payment(
    order_id: str,
    orders_service: ORDERS_SERVICE_DEPENDENCY,
    storefront_id: STOREFRONT_ID_DEPENDENCY
) -> CapturePaymentResponse:
    response = await orders_service.capture_payment(
        storefront_id=storefront_id,
        order_id=order_id
    )
    return response

@router.post("/orders/{order_id:str}/refund")
async def refund_payment(
    order_id: str,
    orders_service: ORDERS_SERVICE_DEPENDENCY,
    storefront_id: STOREFRONT_ID_DEPENDENCY
):
    response = await orders_service.refund_payment(
        storefront_id=storefront_id,
        order_id=order_id
    )
    return response
