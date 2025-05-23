from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from src.dependencies import CURRENT_USER_DEPENDENCY, STOREFRONT_ID_DEPENDENCY
from src.models.product import ProductOut, ProductsOut
from src.schemas.product_metadata import ProductMetadata
from src.schemas.product_query_params import ProductQueryParams
from src.services.products_service import ProductsService

router = APIRouter()


@router.get("/products")
async def get_all_products(
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    products_service: Annotated[ProductsService, Depends()],
    query_params: Annotated[ProductQueryParams, Query()],
    response: Response
) -> list[ProductsOut]:
    response.headers["cache-control"] = "max-age=3600"
    return await products_service.get_all(storefront_id=storefront_id, query_params=query_params)


@router.get("/products/{id:int}")
async def get_product(
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    products_service: Annotated[ProductsService, Depends()],
    id: int,
    response: Response
) -> ProductOut:
    product = await products_service.get(storefront_id=storefront_id, product_id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    response.headers["cache-control"] = "max-age=3600"
    return product


@router.put("/products/{id:int}")
async def update_product(
    current_user: CURRENT_USER_DEPENDENCY,
    products_service: Annotated[ProductsService, Depends()],
    id: int,
    product: ProductOut,
) -> None:
    if not id == product.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mismatching product id.",
        )
    await products_service.update(storefront_id=current_user.storefront_id, product=product)
    return None


@router.get("/products/metadata")
async def get_product_metadata(
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    products_service: Annotated[ProductsService, Depends()],
    response: Response
) -> ProductMetadata:
    response.headers["cache-control"] = "max-age=3600"
    return await products_service.get_product_metadata(storefront_id)
