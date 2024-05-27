from typing import Annotated

from fastapi import Depends

from backend.src.config import SETTINGS_DEPENDENCY
from backend.src.database import ASYNC_SESSION_DEPENDENCY
from backend.src.services.aws_service import AwsService
from backend.src.services.messages_service import MessagesService
from backend.src.services.products_service import ProductsService


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
