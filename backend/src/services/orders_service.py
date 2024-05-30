import base64
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import json
from backend.src.config import Settings
from backend.src.http_client import HttpClient
from backend.src.models.product import Product
from backend.src.models.schemas.create_order_response import CreateOrder
from backend.src.models.schemas.paypal_auth_response import PayPalAuthResponse


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

    async def create_order(self, product_id) -> str:
        statement = select(Product).where(Product.id == product_id)
        results = await self.session.exec(statement=statement)
        product = results.first()

        auth_response = await self._get_access_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{auth_response.token_type} {auth_response.access_token}",
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
            url=f"{self.paypal_url}/v2/checkout/orders", headers=headers, data=json.dumps(data)
        )

        create_order = CreateOrder(**response)

        return create_order.id

    async def _get_access_token(self) -> PayPalAuthResponse:
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

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
