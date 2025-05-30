import base64
import json
from typing import Optional, Type, TypeVar

from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.http_client import HttpClient
from src.models.paypal_settings import PayPalSettings
from src.schemas.create_order_out import CreateOrderOut
from src.schemas.order_update import OrderUpdate
from src.schemas.paypal.auth_response import AuthResponse
from src.schemas.paypal.authorize_payment_response import AuthorizePaymentResponse
from src.schemas.paypal.base import Amount, Breakdown, UnitAmount
from src.schemas.paypal.capture_payment_response import CapturePaymentResponse
from src.schemas.paypal.create_order_payload import CreateOrderPayload
from src.schemas.paypal.create_order_response import CreateOrderResponse
from src.schemas.paypal.item import Item
from src.schemas.paypal.order_details import OrderDetails
from src.schemas.paypal.payments import Authorization
from src.schemas.paypal.purchase_unit import PurchaseUnit
from src.schemas.paypal_credentials import PayPalCredentials
from src.schemas.product_for_order import ProductForOrder
from src.repositories.order_repository import OrderRepository
from src.services.base.payment_processor_base import PaymentProcessorBase


class PayPalService(PaymentProcessorBase):
    """
    Service class for interacting with the PayPal payment API.

    This class provides methods for creating orders, authorizing payments,
    capturing funds, voiding authorizations, reauthorizing payments, and
    issuing refunds using the PayPal REST API.

    It supports dynamic configuration per storefront and assumes a one-to-one
    mapping between a storefront and its associated PayPal credentials.

    Dependencies:
        - `session`: SQLAlchemy AsyncSession used for querying PayPal settings.
        - `settings`: Application-wide settings object.
        - `http_client`: An HTTP client wrapper for sending async requests.
        - `order_repository`: A repository handling order persistence and updates.

    Note:
        This class is intended to be instantiated via the `PaymentProcessorFactory`,
        which injects its required dependencies, including session, settings, and
        services for making HTTP requests and handling order data persistence.
    """

    BASE_URL_AUTHORIZATIONS = "/v2/payments/authorizations"
    BASE_URL_CAPTURES = "/v2/payments/captures"
    BASE_URL_ORDERS = "/v2/checkout/orders"
    T = TypeVar("T")

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
        return self._settings.PAYPAL_BASE_URL
    
    async def get_order(
        self,
        storefront_id: int,
        order_id: str,
        url: str = BASE_URL_ORDERS
    ) -> OrderDetails:
        """
        Retrieve the PayPal order details by ID.

        Args:
            storefront_id (int): ID of the storefront for scoping credentials.
            order_id (str): PayPal order ID to fetch.
            url (str): Base URL segment for order endpoints.

        Returns:
            OrderDetails: Parsed PayPal order data.
        """

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
        """
        Create a new PayPal order based on provided product details.

        Args:
            storefront_id (int): ID of the storefront for credential scoping.
            products (list[ProductForOrder]): List of products to include in the purchase.
            url (str): Base URL segment for order creation.

        Returns:
            CreateOrderOut: Contains the PayPal order ID.
        """

        value = str(sum(product.price for product in products))

        data = CreateOrderPayload(
            purchase_units=[
                PurchaseUnit(
                    amount=Amount(
                        value=value,
                        breakdown=Breakdown(item_total=UnitAmount(value=value))
                    ),
                    items=[
                        Item(
                            name=product.title, 
                            description=product.description, 
                            unit_amount=UnitAmount(value=str(product.price)),
                            quantity="1" # todo: add cart product quantity
                            # todo: add image_url
                        ) for product in products
                    ]
                )
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
        """
        Authorize a PayPal order and persist authorization info.

        Args:
            storefront_id (int): Storefront ID for access control.
            order_id (str): PayPal order ID to authorize.
            product_ids (list[int]): List of internal product IDs associated with the order.
            url (str): URL segment for the authorization endpoint.

        Returns:
            AuthorizePaymentResponse: Response containing authorization details.

        Raises:
            HTTPException: If authorization fails or persistence fails.
        """

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
            # todo: also subtract quantity from product
        except Exception:
            # todo: log and void order
            await self.void_payment(storefront_id, order_id)
            raise HTTPException(status_code=500, detail="Error authorizing payment")
        
    async def reauthorize_payment(self, storefront_id: int, order_id: str, url: str = BASE_URL_AUTHORIZATIONS) -> Authorization:
        """
        Reauthorize a PayPal authorization that is close to expiration.

        Args:
            storefront_id (int): ID of the storefront.
            order_id (str): ID of the PayPal order to reauthorize.
            url (str): URL segment for reauthorization endpoint.

        Returns:
            Authorization: Updated authorization details.
        """

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
        """
        Void a previously authorized PayPal payment.

        Args:
            storefront_id (int): Storefront ID for credential scoping.
            order_id (str): Order ID whose authorization should be voided.
            url (str): URL segment for voiding endpoint.

        Returns:
            Authorization: Response from PayPal indicating void status.
        """

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
        """
        Capture funds for an authorized PayPal order.

        Args:
            storefront_id (int): Storefront ID for credential access.
            order_id (str): Order ID whose funds will be captured.
            url (str): URL segment for the capture endpoint.

        Returns:
            CapturePaymentResponse: Capture transaction details.
        """

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
        """
        Refund a completed PayPal capture.

        Args:
            storefront_id (int): Storefront ID to fetch credentials.
            order_id (str): Order ID whose capture will be refunded.
            url (str): URL segment for the refund endpoint.

        Returns:
            None
        """

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
        """
        Retrieve PayPal client credentials for a given storefront.

        Args:
            storefront_id (int): ID of the storefront.

        Returns:
            PayPalCredentials: Client ID and secret used for token generation.
        """

        statement = select(PayPalSettings).where(PayPalSettings.storefront_id == storefront_id)
        results = await self._session.exec(statement=statement)
        paypal_settings = results.one_or_none()
        return PayPalCredentials(**paypal_settings.model_dump())
    
    async def _get_access_token(self, storefront_id: int) -> AuthResponse:
        """
        Obtain an OAuth2 access token from PayPal.

        Args:
            storefront_id (int): Storefront ID for credential scoping.

        Returns:
            AuthResponse: Contains access token and expiration info.
        """

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
        """
        Send an authenticated request to the PayPal API.

        Args:
            storefront_id (int): Storefront ID to retrieve credentials.
            method (str): HTTP method to use ("GET", "POST").
            path (str): API endpoint path.
            headers (dict, optional): Additional headers to include.
            data (dict, optional): JSON-serializable body data.
            params (dict, optional): URL query parameters.
            response_model (Type[T], optional): Pydantic model to deserialize response into.

        Returns:
            Union[T, dict]: Deserialized response or raw data.
        """
        
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