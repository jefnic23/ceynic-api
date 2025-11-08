from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import selectinload
from sqlmodel import col, select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import SelectOfScalar
from src.database import get_async_session
from src.models.product import Product
from src.models.product_image import ProductImage

class ProductImageRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self._session = session

    async def get_all(self, storefront_id: int, product_id: int) -> list[ProductImage]:
        statement = (
            select(ProductImage)
            .join(Product)
            .where(ProductImage.product_id == product_id)
            .where(Product.storefront_id == storefront_id)
        )
        results = await self._session.exec(statement=statement)
        return results.all()

    async def add_all(
        self, 
        product_images: list[ProductImage]
    ) -> None:
        self._session.add_all(product_images)
        await self._session.commit()

    async def update(
        self,
        product_image: ProductImage,
        position: int
    ) -> ProductImage:
        setattr(product_image, "position", position)  

        await self._session.commit()
        await self._session.refresh(product_image)

        return product_image

    async def delete(
        self, 
        storefront_id: int, 
        product_id: int, 
        public_ids: list[str]
    ) -> None:
        statement = (
            delete(ProductImage)
            .where(ProductImage.product.has(Product.storefront_id == storefront_id))
            .where(ProductImage.product_id == product_id)
            .where(col(ProductImage.public_id).in_(public_ids))
        )
        result = await self._session.exec(statement=statement)
        await self._session.commit()


    async def delete_all(self, storefront_id: int, product_id: int) -> None:
        statement = (
            delete(ProductImage)
            .where(ProductImage.product_id == product_id)
            .where(ProductImage.product.storefront_id == storefront_id)
        )
        await self._session.exec(statement=statement)