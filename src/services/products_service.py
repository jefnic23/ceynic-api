from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import col, select
from sqlmodel.sql.expression import SelectOfScalar

from src.database import ASYNC_SESSION_DEPENDENCY
from src.dependencies import SETTINGS_DEPENDENCY
from src.enums.product_sort_params import ProductSortParams
from src.models.medium import Medium
from src.models.product import Product, ProductForCreate, ProductForUpdate
from src.models.product_image import ProductImage
from src.schemas.product_for_order import ProductForOrder
from src.schemas.product_metadata import MediumCount, PriceRange, ProductMetadata, SizeRanges
from src.schemas.product_query_params import ProductQueryParams
from src.services.product_images_service import ProductImagesService


class ProductsService:
    def __init__(
        self,
        session: ASYNC_SESSION_DEPENDENCY,
        settings: SETTINGS_DEPENDENCY,
        product_images_service: Annotated[ProductImagesService, Depends()],
    ):
        self._session = session
        self._settings = settings
        self._product_images_service = product_images_service

    async def get_all(self, storefront_id: int, query_params: ProductQueryParams | None = None) -> list[Product]:
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

    async def get(self, storefront_id: int, product_id: int) -> Product:
        statement = (
            select(Product)
            .where(Product.storefront_id == storefront_id)
            .where(Product.id == product_id)
            .options(selectinload(Product.medium), selectinload(Product.images))
        )
        results = await self._session.exec(statement=statement)
        product = results.one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def get_for_order(self, storefront_id: int, product_ids: list[int]) -> list[ProductForOrder]:
        # todo: consolidate this method with `get` above
        statement = (
            select(Product)
            .where(Product.storefront_id == storefront_id)
            .where(col(Product.id).in_(product_ids))
            .options(selectinload(Product.medium), selectinload(Product.images))
        )
        results = await self._session.exec(statement=statement)
        return results.all()

    async def create(self, storefront_id: int, product_in: ProductForCreate) -> None:
        product = Product(**product_in.model_dump(exclude_unset=True), storefront_id=storefront_id)
        self._session.add(product)
        await self._session.flush()

        for index, file in enumerate(product_in.images, 1):
            product_image = await self._product_images_service.create_and_upload(
                product=product, file=file, position=index
            )
            self._session.add(product_image)

        await self._session.commit()

    async def update(self, storefront_id: int, product_in: ProductForUpdate) -> None:
        statement = (
            select(Product)
            .where(Product.storefront_id == storefront_id)
            .where(Product.id == product_in.id)
            .options(selectinload(Product.images))
        )
        results = await self._session.exec(statement=statement)
        product = results.one_or_none()

        if not product:
            return

        update_data = product_in.model_dump(exclude_unset=True, exclude={"id", "images"})

        if not update_data and product_in.images is None:
            return

        for key, value in update_data.items():
            setattr(product, key, value)

        if product_in.images is not None:
            existing_images = {Path(image.url).stem: image for image in product.images}

            for position, file in enumerate(product_in.images, 1):
                image_metadata = await self._product_images_service.get_image_metadata(product, file)
                image = existing_images.pop(image_metadata.file_hash, None)
                if image is not None:
                    image.position = position
                    continue

                if not await self._product_images_service.upload(image_metadata):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to upload product image.",
                    )
                self._session.add(
                    ProductImage(
                        url=image_metadata.download_url,
                        position=position,
                        width=image_metadata.width,
                        height=image_metadata.height,
                        product=product,
                    )
                )

            for image in existing_images.values():
                if not await self._product_images_service.delete(product=product, image=image):
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Failed to delete product image.",
                    )
                await self._session.delete(image)

        await self._session.commit()

    async def delete(self, storefront_id: int, product_id: int) -> None:
        statement = (
            select(Product)
            .where(Product.storefront_id == storefront_id)
            .where(Product.id == product_id)
            .options(selectinload(Product.images))
        )
        results = await self._session.exec(statement=statement)
        product = results.one_or_none()

        # first, delete images from bunny
        for image in product.images:
            if not await self._product_images_service.delete(product=product, image=image):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to delete product image.",
                )

        # then, delete the product (images cascade delete)
        await self._session.delete(product)

        await self._session.commit()

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
        price_size_statement = select(
            func.min(Product.price).label("minimum"),
            func.max(Product.price).label("maximum"),
            func.min(Product.width).label("width_minimum"),
            func.max(Product.width).label("width_maximum"),
            func.min(Product.height).label("height_minimum"),
            func.max(Product.height).label("height_maximum"),
        ).where(Product.storefront_id == storefront_id)
        price_size_results = await self._session.exec(price_size_statement)
        min_price, max_price, width_minimum, width_maximum, height_minimum, height_maximum = (
            price_size_results.one_or_none()
        )

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
            size_ranges=SizeRanges(
                width_minimum=width_minimum,
                width_maximum=width_maximum,
                height_minimum=height_minimum,
                height_maximum=height_maximum,
            ),
        )

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
                statement = statement.order_by(Product.height.desc(), Product.width.desc())
            else:
                statement = statement.order_by(Product.id)
        return statement

    # async def _get_product_images(self, storefront_id: int, product_id: int) -> list[ProductImage]:
    #     statement = (
    #         select(ProductImage)
    #         .join(Product)
    #         .where(ProductImage.product_id == product_id)
    #         .where(Product.storefront_id == storefront_id)
    #     )
    #     results = await self._session.exec(statement=statement)
    #     return results.all()
