from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import selectinload
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import SelectOfScalar

from src.database import get_async_session
from src.enums.product_sort_params import ProductSortParams
from src.models.medium import Medium
from src.models.product import Product, ProductIn, ProductOut
from src.models.product_image import ProductImage
from src.schemas.product_for_order import ProductForOrder
from src.schemas.product_query_params import ProductQueryParams


class ProductRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self._session: AsyncSession = session

    async def get_all(
        self, 
        storefront_id: int, 
        query_params: ProductQueryParams | None = None
    ) -> list[ProductOut]:
        statement = (
            select(Product)
            .join(ProductImage)
            .where(Product.storefront_id == storefront_id)
            .where(ProductImage.position == 1)
            .options(selectinload(Product.medium), selectinload(Product.images))
        )
        if query_params:
            statement = self._apply_query_params(statement, query_params)
        results = await self._session.exec(statement=statement)
        return results.all()
    
    async def get(self, storefront_id: int, product_id: int) -> ProductOut | None:
        # should this and the method above return the base Product? And let the routers/service determine what the return type should be?
        statement = (
            select(Product)
            .where(Product.storefront_id == storefront_id)
            .where(Product.id == product_id)
            .options(selectinload(Product.medium), selectinload(Product.images))
        )
        results = await self._session.exec(statement=statement)
        return results.one_or_none()
    
    async def get_many(self, storefront_id: int, product_ids: list[int]) -> list[ProductForOrder]:
        statement = (
            select(Product)
            .where(Product.storefront_id == storefront_id)
            .where(col(Product.id).in_(product_ids))
            .options(selectinload(Product.medium), selectinload(Product.images))
        )
        results = await self._session.exec(statement=statement)
        return results.all()
    
    async def update(self, storefront_id: int, product_id: int, updates: ProductIn) -> Product | None:
        statement = select(Product).where(Product.storefront_id == storefront_id).where(Product.id == product_id)
        results = await self._session.exec(statement=statement)
        product = results.one_or_none()
        if not product:
            return
        
        update_data = updates.model_dump(exclude_unset=True, exclude={"images"})
        if not update_data:
            return
        
        for key, value in update_data.items():
            setattr(product, key, value)

        await self._session.commit()
        await self._session.refresh(product)

        return product

    @staticmethod
    def _apply_query_params(statement: SelectOfScalar, query_params: ProductQueryParams | None) -> SelectOfScalar:
        if query_params.medium:
            statement = statement.where(col(Medium.name).in_(query_params.medium))
        if query_params.min_price:
            statement = statement.where(Product.price >= query_params.min_price)
        if query_params.max_price:
            statement = statement.where(Product.price <= query_params.max_price)
        if query_params.min_width:
            statement = statement.where(Product.width >= query_params.min_width)
        if query_params.max_width:
            statement = statement.where(Product.width <= query_params.max_width)
        if query_params.min_height:
            statement = statement.where(Product.height >= query_params.min_height)
        if query_params.max_height:
            statement = statement.where(Product.height <= query_params.max_height)
        if query_params.sort:
            if query_params.sort == ProductSortParams.OLDEST:
                statement = statement.order_by(Product.date_added)
            elif query_params.sort == ProductSortParams.NEWEST:
                statement = statement.order_by(Product.date_added.desc())
            elif query_params.sort == ProductSortParams.PRICE_ASC:
                statement = statement.order_by(Product.price)
            elif query_params.sort == ProductSortParams.PRICE_DESC:
                statement = statement.order_by(Product.price.desc())
            elif query_params.sort == ProductSortParams.SIZE_ASC:
                statement = statement.order_by(Product.height, Product.width)
            elif query_params.sort == ProductSortParams.SIZE_DESC:
                statement = statement.order_by(
                    Product.height.desc(), Product.width.desc()
                )
            else:
                statement = statement.order_by(Product.id)
        return statement