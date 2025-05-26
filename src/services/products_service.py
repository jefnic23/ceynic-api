from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings, get_settings
from src.database import get_async_session
from src.models.medium import Medium
from src.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.models.product import ProductOut
from src.schemas.product_for_order import ProductForOrder
from src.schemas.product_metadata import MediumCount, PriceRange, ProductMetadata, SizeRanges
from src.schemas.product_query_params import ProductQueryParams
from src.models.storefront import Storefront
from src.services.aws_service import AwsService


class ProductsService:
    def __init__(
        self, 
        session: Annotated[AsyncSession, Depends(get_async_session)], 
        settings: Annotated[Settings, Depends(get_settings)], 
        aws: Annotated[AwsService, Depends()],
        repository: Annotated[ProductRepository, Depends()] 
    ):
        self._session = session
        self._settings = settings
        self._aws = aws
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
        statement = (
            select(Product)
            .join(Storefront, Product.storefront_id == Storefront.id)
            .where(Storefront.id == storefront_id)
            .where(col(Product.id).in_(product_ids))
        )
        results = await self._session.exec(statement=statement)
        products = results.all()
        return [ProductForOrder(**product.model_dump()) for product in products]

    async def update(self, storefront_id: int, product: ProductOut) -> None:
        # todo: implement
        statement = select(Product).where(Product.id == product.id).where(Storefront.id == storefront_id)
        results = await self._session.exec(statement=statement)
        product_to_update = results.one()

    async def get_product_metadata(self, storefront_id: int) -> ProductMetadata:
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
