from fastapi import APIRouter, HTTPException, status

from src.dependencies import (
    CURRENT_USER_DEPENDENCY,
    PRODUCTS_SERVICE_DEPENDENCY,
    SUBDOMAIN_DEPENDENCY,
    USERS_SERVICE_DEPENDENCY,
)
from src.models.enums.product_sort_params import ProductSortParams
from src.models.schemas.medium_count import MediumCount
from src.models.schemas.price_range import PriceRange
from src.models.schemas.product import ProductOut, ProductsOut
from src.models.schemas.size_ranges import SizeRanges

router = APIRouter()


@router.get("/products")
async def get_all_products(
    subdomain: SUBDOMAIN_DEPENDENCY,
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    sort: ProductSortParams | None = None,
) -> list[ProductsOut]:
    return await products_service.get_all(subdomain=subdomain, sort=sort)


@router.get("/products/{id:int}")
async def get_product(
    subdomain: SUBDOMAIN_DEPENDENCY,
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    id: int
) -> ProductOut:
    product = await products_service.get(product_id=id, subdomain=subdomain)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.put("/products/{id:int}")
async def update_product(
    current_user: CURRENT_USER_DEPENDENCY,
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
    users_service: USERS_SERVICE_DEPENDENCY,
    id: int,
    product: ProductOut,
) -> None:
    if not id == product.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mismatching product id.",
        )
    subdomain = await users_service.get_subdomain_from_user(id=current_user.id)
    old_product = await products_service.get(product_id=id, subdomain=subdomain)
    if not old_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    await products_service.update(product=product)
    return None


@router.get("/products/priceRange")
async def get_price_range(
    subdomain: SUBDOMAIN_DEPENDENCY,
    products_service: PRODUCTS_SERVICE_DEPENDENCY, 
) -> PriceRange:
    return await products_service.get_price_range(subdomain=subdomain)


@router.get("/products/mediumCounts")
async def get_medium_counts(
    subdomain: SUBDOMAIN_DEPENDENCY,
    products_service: PRODUCTS_SERVICE_DEPENDENCY,
) -> list[MediumCount]:
    return await products_service.get_medium_counts(subdomain=subdomain)


@router.get("/products/sizeRanges")
async def get_size_ranges(
    subdomain: SUBDOMAIN_DEPENDENCY,
    products_service: PRODUCTS_SERVICE_DEPENDENCY, 
) -> SizeRanges:
    return await products_service.get_size_ranges(subdomain=subdomain)
