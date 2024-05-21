from backend.src.dependencies import PRODUCTS_SERVICE_DEPENDENCY
from fastapi import APIRouter, HTTPException, status

from backend.src.models.product import Product

router = APIRouter()


@router.get("/products")
async def get_all_services(
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
) -> list[Product]:
    return await products_service.get_all()


@router.get("/products/{id}")
async def get_service(
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    id: int,
) -> Product:
    product = await products_service.get(id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product
