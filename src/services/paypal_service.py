import base64
import json
from typing import Optional, Type, TypeVar

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.http_client import HttpClient
from src.models.paypal_settings import PayPalSettings
from src.models.schemas.create_order_out import CreateOrderOut
from src.models.schemas.order_update import OrderUpdate
from src.models.schemas.paypal.auth_response import AuthResponse
from src.models.schemas.paypal.authorize_payment_response import AuthorizePaymentResponse
from src.models.schemas.paypal.base import Amount
from src.models.schemas.paypal.capture_payment_response import CapturePaymentResponse
from src.models.schemas.paypal.create_order_payload import CreateOrderPayload
from src.models.schemas.paypal.create_order_response import CreateOrderResponse
from src.models.schemas.paypal.order_details import OrderDetails
from src.models.schemas.paypal.payments import Authorization
from src.models.schemas.paypal.purchase_unit import PurchaseUnit
from src.models.schemas.paypal_credentials import PayPalCredentials
from src.models.schemas.product_for_order import ProductForOrder
from src.repositories.order_repository import OrderRepository
from src.services.base.payment_processor_base import PaymentProcessorBase

T = TypeVar("T")


class PayPalService(PaymentProcessorBase):
    BASE_URL_AUTHORIZATIONS = "/v2/payments/authorizations"
    BASE_URL_CAPTURES = "/v2/payments/captures"
    BASE_URL_ORDERS = "/v2/checkout/orders"

    def __init__(
        self, 
        session: AsyncSession, 
        settings: Settings, 
        http_client: HttpClient,
        order_repository: OrderRepository
    ):
        self._session: AsyncSession = session
        self._settings: Settings = settings
        self._http_client: HttpClient = http_client
        self._order_repository: OrderRepository = order_repository

        # todo: cache paypal access tokens in redis using dict[storefront_id, token]
        # token should have expiration time, so use that to determine when to get a new token
        self._access_token: str | None = None

    @property
    def _paypal_url(self) -> str:
        return self._settings.PAYPAL_URL
    
    async def get_order(
        self,
        storefront_id: int,
        order_id: str,
        url: str = BASE_URL_ORDERS
    ) -> OrderDetails:
        order_response = await self._send_request(
            storefront_id=storefront_id, 
            method="GET", 
            path=f"{url}/{order_id}",
            response_model=OrderDetails
        )

        # todo: also get authorization details
        # statement = select(Order).where(Order.id == order_id)
        # results = await self._session.exec(statement=statement)
        # order = results.one_or_none()
        # authorization_id = order.authorization_id

        # authorization_response = await self._send_request(
        #     storefront_id=storefront_id,
        #     method="GET", 
        #     path=f"{url}/{authorization_id}",
        #     response_model=OrderDetails)

        return order_response
        
    
    async def create_order(
        self, 
        storefront_id: int, 
        products: list[ProductForOrder], 
        url: str = BASE_URL_ORDERS
    ) -> CreateOrderOut:
        data = CreateOrderPayload(
            purchase_units=[
                PurchaseUnit(
                    description=product.title, 
                    amount=Amount(value=product.price)
                ) 
                for product in products
            ]
        )

        response = await self._send_request(
            storefront_id=storefront_id, 
            method="POST", 
            path=url, 
            data=data.model_dump(mode="json"),
            response_model=CreateOrderResponse
        )

        return CreateOrderOut(order_id=response.id)
    
    async def authorize_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        product_ids: list[int], 
        url: str = BASE_URL_ORDERS
    ) -> AuthorizePaymentResponse:
        response = await self._send_request(
            storefront_id=storefront_id, 
            method="POST", 
            path=f"{url}/{order_id}/authorize",
            response_model=AuthorizePaymentResponse
        )

        try:
            await self._order_repository.create(
                order_id=order_id,
                create_time=response.create_time,
                storefront_id=storefront_id,
                authorization_id=response.authorization_id,
                status="PENDING", # todo: make this an enum
                product_ids=product_ids
            )
            return response
        except Exception:
            # todo: log and void order
            await self.void_payment(storefront_id, order_id)
            raise HTTPException(status_code=500, detail="Error authorizing payment")
        
    async def reauthorize_payment(self, storefront_id: int, order_id: str, url: str = BASE_URL_AUTHORIZATIONS) -> Authorization:
        order = await self._order_repository.get(storefront_id=storefront_id, order_id=order_id)

        response = await self._send_request(
            storefront_id=storefront_id, 
            method="POST", 
            path=f"{url}/{order.authorization_id}/reauthorize",
            headers={"Prefer": "return=representation"},
            response_model=Authorization
        )

        await self._order_repository.update(
            storefront_id=storefront_id,
            order_id=order_id,
            updates=OrderUpdate(
                status="PENDING", 
                authorization_id=response.id
            )
        )

        return response
        
    async def void_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        url: str = BASE_URL_AUTHORIZATIONS
    ) -> Authorization:
        order = await self._order_repository.get(storefront_id=storefront_id, order_id=order_id)

        response = await self._send_request(
            storefront_id=storefront_id, 
            method="POST", 
            path=f"{url}/{order.authorization_id}/void",
            headers={"Prefer": "return=representation"},
            response_model=Authorization
        )

        await self._order_repository.update(
            storefront_id=storefront_id,
            order_id=order_id,
            updates=OrderUpdate(status=response.status)
        )

        return response
    
    async def capture_payment(
        self, storefront_id: int, order_id: str, url: str = BASE_URL_AUTHORIZATIONS
    ) -> CapturePaymentResponse:
        order = await self._order_repository.get(storefront_id=storefront_id, order_id=order_id)

        response = await self._send_request(
            storefront_id=storefront_id, 
            method="POST", 
            path=f"{url}/{order.authorization_id}/capture",
            headers={"Prefer": "return=representation"},
            response_model=CapturePaymentResponse
        )

        # todo: handle reauthorization here

        await self._order_repository.update(
            storefront_id=storefront_id,
            order_id=order_id,
            updates=OrderUpdate(capture_id=response.id, status="COMPLETED")
        )

        return response
    
    async def refund_payment(
        self, 
        storefront_id: int, 
        order_id: str, 
        url: str = BASE_URL_CAPTURES
    ):
        # todo: capture response
        order = await self._order_repository.get(storefront_id=storefront_id, order_id=order_id)

        await self._send_request(
            storefront_id=storefront_id, 
            method="POST", 
            path=f"{url}/{order.capture_id}/refund",
            headers={"Prefer": "return=representation"}
        )
    
        await self._order_repository.update(
            storefront_id=storefront_id,
            order_id=order_id,
            updates=OrderUpdate(status="REFUNDED")
        )
    
    # region Private Methods

    async def _get_credentials(self, storefront_id: int) -> PayPalCredentials:
        statement = select(PayPalSettings).where(PayPalSettings.storefront_id == storefront_id)
        results = await self._session.exec(statement=statement)
        paypal_settings = results.one_or_none()
        return PayPalCredentials(**paypal_settings.model_dump())
    
    async def _get_access_token(self, storefront_id: int) -> AuthResponse:
        # todo: error handling
        paypal_credentials = await self._get_credentials(storefront_id)
        
        auth = base64.b64encode(
            f"{paypal_credentials.client_id}:{paypal_credentials.client_secret}".encode()
        ).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth}",
        }

        data = {"grant_type": "client_credentials"}

        response = await self._http_client.post_async(
            url=f"{self._paypal_url}/v1/oauth2/token",
            data=data,
            headers=headers,
        )

        return AuthResponse(**response)
    
    async def _send_request(
        self, 
        storefront_id: int,
        method: str, 
        path: str, 
        headers: dict[str, any] = None,
        data: dict[str, any] = None, 
        params: dict[str, any] = None,
        response_model: Optional[Type[T]] = None
    ) -> T | dict[str, any]:
        # todo: implement redis to cache dict of storefront access_tokens
        if not self._access_token:
            auth_response = await self._get_access_token(storefront_id)
            self._access_token = auth_response.access_token

        request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._access_token}",
            **(headers if isinstance(headers, dict) else {})
        }

        url = f"{self._paypal_url}{path}"

        if method.upper() == "GET":
            response_data = await self._http_client.get_async(url=url, headers=request_headers, params=json.dumps(params))
        elif method.upper() == "POST":
            response_data = await self._http_client.post_async(
                url=url,
                headers=request_headers,
                data=json.dumps(data) if data else "{}",
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        try:
            if response_model:
                return response_model(**response_data)
        except Exception as ex:
            # todo: log exception and response
            print(f"failed to deserialize: {ex}")

        return response_data

    # endregion