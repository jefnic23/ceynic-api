from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings, get_settings
from src.database import get_async_session
from src.models.medium import Medium
from src.models.product import Product, ProductIn
from src.repositories.product_repository import ProductRepository
from src.models.product import ProductOut
from src.schemas.product_for_order import ProductForOrder
from src.schemas.product_metadata import MediumCount, PriceRange, ProductMetadata, SizeRanges
from src.schemas.product_query_params import ProductQueryParams
from src.models.storefront import Storefront
from src.services.product_images_service import ProductImagesService


class ProductsService:
    def __init__(
        self, 
        session: Annotated[AsyncSession, Depends(get_async_session)], 
        settings: Annotated[Settings, Depends(get_settings)],
        repository: Annotated[ProductRepository, Depends()]
    ):
        self._session = session
        self._settings = settings
        self._repository = repository

    async def get_all(
        self, storefront_id: int, query_params: ProductQueryParams | None = None
    ) -> list[ProductOut]:
        products = await self._repository.get_all(storefront_id=storefront_id, query_params=query_params)
        return products

    async def get(self, storefront_id: int, product_id: int) -> ProductOut:
        product = await self._repository.get(storefront_id=storefront_id, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product
    
    async def get_for_order(self, storefront_id: int, product_ids: list[int]) -> list[ProductForOrder]:
        products = await self._repository.get_many(storefront_id, product_ids)
        return products

    async def update(self, storefront_id: int, product: ProductIn) -> ProductOut:
        product = await self._repository.update(storefront_id, product.id, product)
        return product

    async def get_product_metadata(self, storefront_id: int) -> ProductMetadata:
        """
        Retrieve metadata for products associated with a given storefront ID.

        This function asynchronously fetches the following metadata for products linked to a specified `storefront_id`:
        - The minimum and maximum price of the products.
        - The minimum and maximum dimensions (width and height) of the products.
        - The count of each medium type used in the products.

        Args:
            storefront_id (int): The identifier for the storefront whose product metadata is to be retrieved.

        Returns:
            ProductMetadata: An object containing the price range, size ranges, and counts of mediums used in products.
        """
        # these could probably all be views
        price_size_statement = (
            select(
                func.min(Product.price).label("minimum"),
                func.max(Product.price).label("maximum"),
                func.min(Product.width).label("width_minimum"),
                func.max(Product.width).label("width_maximum"),
                func.min(Product.height).label("height_minimum"),
                func.max(Product.height).label("height_maximum"),
            )
            .where(Product.storefront_id == storefront_id)
        )
        price_size_results = await self._session.exec(price_size_statement)
        min_price, max_price, width_minimum, width_maximum, height_minimum, height_maximum = price_size_results.one_or_none()

        medium_statement = (
            select(Medium.id, Medium.name, func.count(Product.medium_id).label("count"))
            .select_from(Medium)
            .join(Product, Medium.id == Product.medium_id, isouter=True)
            .where(Product.storefront_id == storefront_id)
            .group_by(Medium.id, Medium.name)
        )
        medium_results = await self._session.exec(medium_statement)
        medium_counts = [
            MediumCount(id=medium_count[0], name=medium_count[1], count=medium_count[2])
            for medium_count in medium_results.all()
        ] 

        return ProductMetadata(
            price_range=PriceRange(minimum=min_price, maximum=max_price),
            medium_counts=medium_counts,
            size_ranges=SizeRanges(width_minimum=width_minimum, width_maximum=width_maximum, height_minimum=height_minimum, height_maximum=height_maximum)
        )
