from fastapi import APIRouter, HTTPException, status

from src.dependencies import PRODUCTS_SERVICE_DEPENDENCY
from src.models.enums.product_sort_params import ProductSortParams
from src.models.schemas.product import ProductOut, ProductsOut

router = APIRouter()


@router.get("/products")
async def get_all_products(
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    sort: ProductSortParams | None = None,
) -> list[ProductsOut]:
    return await products_service.get_all(sort=sort)


@router.get("/products/{id}")
async def get_product(
    id: int,
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
) -> ProductOut:
    product = await products_service.get(product_id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
