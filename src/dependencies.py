from typing import Annotated

import aiohttp
from fastapi import Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from src.config import SETTINGS_DEPENDENCY
from src.database import ASYNC_SESSION_DEPENDENCY
from src.exceptions import credentials_exception
from src.http_client import HTTP_CLIENT_DEPENDENCY
from src.models.schemas.recaptcha import ReCaptchaResponse
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.aws_service import AwsService
from src.services.messages_service import MessagesService
from src.services.orders_service import OrdersService
from src.services.products_service import ProductsService
from src.services.refresh_tokens_service import RefreshTokensService
from src.services.users_service import UsersService

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
OAUTH_DEPENDENCY = Annotated[str, Depends(OAUTH2_SCHEME)]


async def get_aws_service(
    session: ASYNC_SESSION_DEPENDENCY, settings: SETTINGS_DEPENDENCY
) -> AwsService:
    return AwsService(session=session, settings=settings)


AWS_SERVICE_DEPENDENCY = Annotated[AwsService, Depends(get_aws_service)]


async def get_products_service(
    session: ASYNC_SESSION_DEPENDENCY,
    settings: SETTINGS_DEPENDENCY,
    aws: AWS_SERVICE_DEPENDENCY,
) -> ProductsService:
    return ProductsService(session=session, settings=settings, aws=aws)


PRODUCTS_SERVICE_DEPENDENCY = Annotated[ProductsService, Depends(get_products_service)]


async def get_messages_service(settings: SETTINGS_DEPENDENCY) -> MessagesService:
    return MessagesService(settings=settings)


MESSAGES_SERVICE_DEPENDENCY = Annotated[MessagesService, Depends(get_messages_service)]


async def get_orders_service(
    session: ASYNC_SESSION_DEPENDENCY,
    settings: SETTINGS_DEPENDENCY,
    http_client: HTTP_CLIENT_DEPENDENCY,
) -> OrdersService:
    return OrdersService(session=session, settings=settings, http_client=http_client)


ORDERS_SERVICE_DEPENDENCY = Annotated[OrdersService, Depends(get_orders_service)]


async def get_users_service(
    session: ASYNC_SESSION_DEPENDENCY,
) -> UsersService:
    return UsersService(session=session)


USERS_SERVICE_DEPENDENCY = Annotated[UsersService, Depends(get_users_service)]


async def get_refresh_tokens_service(
    session: ASYNC_SESSION_DEPENDENCY,
) -> RefreshTokensService:
    return RefreshTokensService(session=session)


REFRESH_TOKENS_SERVICE_DEPENDENCY = Annotated[
    RefreshTokensService, Depends(get_refresh_tokens_service)
]


async def get_auth_service(
    session: ASYNC_SESSION_DEPENDENCY,
    settings: SETTINGS_DEPENDENCY,
    users_service: USERS_SERVICE_DEPENDENCY,
    refresh_tokens_service: REFRESH_TOKENS_SERVICE_DEPENDENCY,
) -> AuthService:
    return AuthService(
        session=session,
        settings=settings,
        users_service=users_service,
        refresh_tokens_service=refresh_tokens_service,
    )


AUTH_SERVICE_DEPENDENCY = Annotated[AuthService, Depends(get_auth_service)]


async def verify_recaptcha(
    token: Annotated[str, Form()], request: Request, settings: SETTINGS_DEPENDENCY
) -> None:
    async with aiohttp.ClientSession() as session:
        data = {
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
            "remoteip": request.client.host,
        }
        async with session.post(
            url="https://www.google.com/recaptcha/api/siteverify", data=data
        ) as response:
            if not response.ok:
                await response.raise_for_status()
            response_data = await response.json()
            recaptcha_response = ReCaptchaResponse(**response_data)
            if not recaptcha_response.success:
                # TODO: log recaptcha_response.error_codes
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
            if recaptcha_response.score < 0.9:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_current_user(
    token: OAUTH_DEPENDENCY,
    users_service: USERS_SERVICE_DEPENDENCY,
    auth_service: AUTH_SERVICE_DEPENDENCY,
) -> User:
    payload = auth_service.verify_token(token)
    user = await users_service.get_user_by_id(id=int(payload.get("sub")))
    if user is None:
        raise credentials_exception
    return user


CURRENT_USER_DEPENDENCY = Annotated[User, Depends(get_current_user)]


def get_subdomain(request: Request) -> str:
    """
    Extracts the subdomain from the incoming request's host header.
    """

    # todo: this should probably be used only on prod env

    host = request.headers.get("host")
    if not host:
        raise HTTPException(status_code=400, detail="Host header is missing")

    # Assuming the main domain is 'ceynic.net'
    main_domain = "ceynic.net" # todo: environment variable?
    if not host.endswith(main_domain):
        raise HTTPException(status_code=400, detail="Invalid host")

    # Extract the subdomain
    subdomain = host.removesuffix(f".{main_domain}").split(".")[0]

    if not subdomain:
        raise HTTPException(status_code=400, detail="Subdomain is missing")
    
    # todo: get and return storefront id?

    return subdomain


SUBDOMAIN_DEPENDENCY = Annotated[str, Depends(get_subdomain)]
