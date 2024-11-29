import base64
import json

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.http_client import HttpClient
from src.models.order import Order
from src.models.product import Product
from src.models.schemas.paypal import (
    CapturePaymentResponse,
    CreateOrderResponse,
    PayPalAuthResponse,
)


class OrdersService:
    def __init__(
        self, session: AsyncSession, settings: Settings, http_client: HttpClient
    ):
        self.session: AsyncSession = session
        self.client_id: str = settings.PAYPAL_CLIENT_ID
        self.client_secret: str = settings.PAYPAL_CLIENT_SECRET
        self.paypal_url: str = settings.PAYPAL_URL
        self.http_client: HttpClient = http_client
        self.access_token: str = None

    async def create_order(self, product_id: int) -> str:
        statement = select(Product).where(Product.id == product_id)
        results = await self.session.exec(statement=statement)
        product = results.first()

        if not self.access_token:
            auth_response = await self._get_access_token()
            self.access_token = auth_response.access_token

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "description": product.description,
                    "amount": {"currency_code": "USD", "value": str(product.price)},
                }
            ],
        }

        response = await self.http_client.post_async(
            url=f"{self.paypal_url}/v2/checkout/orders",
            headers=headers,
            data=json.dumps(data),
        )

        create_order_response = CreateOrderResponse(**response)

        return create_order_response.id

    async def capture_payment(
        self, order_id: str, product_id: str
    ) -> CapturePaymentResponse:
        if not self.access_token:
            auth_response = await self._get_access_token()
            self.access_token = auth_response.access_token

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        response = await self.http_client.post_async(
            url=f"{self.paypal_url}/v2/checkout/orders/{order_id}/capture",
            data={},
            headers=headers,
        )

        capture_payment_response = CapturePaymentResponse(**response)

        statement = select(Product).where(Product.id == product_id)
        results = await self.session.exec(statement=statement)
        product = results.first()
        product.sold = True
        product.order_id = order_id

        order = Order(id=capture_payment_response.id)
        self.session.add(order)
        await self.session.commit()

        return capture_payment_response

    # TODO: write method that checks for/validates existing token

    async def _get_access_token(self) -> PayPalAuthResponse:
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth}",
        }

        data = {"grant_type": "client_credentials"}

        response = await self.http_client.post_async(
            url=f"{self.paypal_url}/v1/oauth2/token",
            data=data,
            headers=headers,
        )

        return PayPalAuthResponse(**response)
