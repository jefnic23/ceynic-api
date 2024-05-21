from typing import Annotated

from fastapi import Depends

from backend.src.config import SETTINGS_DEPENDENCY
from backend.src.database import ASYNC_SESSION_DEPENDENCY
from backend.src.services.products_service import ProductsService


async def get_products_service(
    session: ASYNC_SESSION_DEPENDENCY,
    settings: SETTINGS_DEPENDENCY,
) -> ProductsService:
    return ProductsService(session=session, settings=settings)


PRODUCTS_SERVICE_DEPENDENCY = Annotated[ProductsService, Depends(get_products_service)]
