from typing import Annotated

import aiohttp
from fastapi import Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from src.config import SETTINGS_DEPENDENCY
from src.exceptions import credentials_exception
from src.schemas.recaptcha import ReCaptchaResponse
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.storefronts_service import StorefrontsService
from src.services.users_service import UsersService


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
OAUTH_DEPENDENCY = Annotated[str, Depends(OAUTH2_SCHEME)]


async def verify_recaptcha(
    settings: SETTINGS_DEPENDENCY, token: Annotated[str, Form()], request: Request
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
    users_service: Annotated[UsersService, Depends()],
    auth_service: Annotated[AuthService, Depends()],
) -> User:
    payload = auth_service.verify_token(token)
    user = await users_service.get_user_by_id(id=int(payload.get("sub")))
    if user is None:
        raise credentials_exception
    return user


CURRENT_USER_DEPENDENCY = Annotated[User, Depends(get_current_user)]


def get_subdomain(settings: SETTINGS_DEPENDENCY, request: Request) -> str:
    """
    Extracts the subdomain from the incoming request's host header.
    """
    if settings.FASTAPI_ENV == "development":
        return "traceynicholas"

    host = request.headers.get("host")
    if not host:
        raise HTTPException(status_code=400, detail="Host header is missing")

    # Assuming the main domain is 'ceynic.net'
    main_domain = "ceynic.net"
    if not host.endswith(main_domain):
        raise HTTPException(status_code=400, detail="Invalid host")

    # Extract the subdomain
    subdomain = host.removesuffix(f".{main_domain}").split(".")[0]

    if not subdomain:
        raise HTTPException(status_code=400, detail="Subdomain is missing")

    # todo: get and return storefront id?

    return subdomain


SUBDOMAIN_DEPENDENCY = Annotated[str, Depends(get_subdomain)]


async def get_storefront_id(
    storefronts_service: Annotated[StorefrontsService, Depends()],
    subdomain: Annotated[str, Depends(get_subdomain)]
) -> int:
    return await storefronts_service.get_id_from_subdomain(subdomain=subdomain)


STOREFRONT_ID_DEPENDENCY = Annotated[int, Depends(get_storefront_id)]
