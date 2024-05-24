from fastapi import APIRouter, HTTPException, status

from backend.src.dependencies import PRODUCTS_SERVICE_DEPENDENCY
from backend.src.models.schemas.product import ProductOut, ProductsOut

router = APIRouter()


@router.get("/products")
async def get_all_products(
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
) -> list[ProductsOut]:
    return await products_service.get_all()


@router.get("/products/{id}")
async def get_product(
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    id: int,
) -> ProductOut:
    product = await products_service.get(id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
