from typing import Annotated

from fastapi import Depends

from backend.src.database import ASYNC_SESSION_DEPENDENCY
from backend.src.services.products_service import ProductsService


async def get_products_service(session: ASYNC_SESSION_DEPENDENCY) -> ProductsService:
    return ProductsService(session=session)


PRODUCTS_SERVICE_DEPENDENCY = Annotated[ProductsService, Depends(get_products_service)]