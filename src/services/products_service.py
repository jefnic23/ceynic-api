from sqlalchemy import Select, func
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.models.enums.product_sort_params import ProductSortParams
from src.models.medium import Medium
from src.models.product import Product
from src.models.schemas.medium_count import MediumCount
from src.models.schemas.price_range import PriceRange
from src.models.schemas.product import ProductOut, ProductsOut
from src.models.schemas.product_for_order import ProductForOrder
from src.models.schemas.product_query_params import ProductQueryParams
from src.models.schemas.size_ranges import SizeRanges
from src.models.storefront import Storefront
from src.services.aws_service import AwsService


class ProductsService:
    def __init__(self, session: AsyncSession, settings: Settings, aws: AwsService):
        self.session = session
        self.settings = settings
        self.aws = aws

    async def get_all(
        self, subdomain: str, query_params: ProductQueryParams | None = None
    ) -> list[ProductsOut]:
        statement = (
            select(Product)
            .join(Medium, Product.medium_id == Medium.id)
            .join(Storefront, Product.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
            .where(Product.thumbnail != None)
        )
        if query_params:
            statement = self.apply_query_params(statement, query_params)
        results = await self.session.exec(statement=statement)
        products: list[Product] = results.all()
        return [
            ProductsOut(
                **product.model_dump(),
                image_url=self.aws.get_product_thumbnail(product),
            )
            for product in products
        ]

    async def get(self, product_id: int, subdomain: str) -> ProductOut:
        statement = (
            select(Product)
            .join(Storefront, Product.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
            .where(Product.id == product_id)
        )
        results = await self.session.exec(statement=statement)
        product: Product = results.one()
        images = await self.aws.get_product_images(product)
        return ProductOut(
            **product.model_dump(),
            images=images,
        )
    
    async def get_for_order(self, storefront_id: int, product_ids: list[int]) -> list[ProductForOrder]:
        statement = (
            select(Product)
            .join(Storefront, Product.storefront_id == Storefront.id)
            .where(Storefront.id == storefront_id)
            .where(col(Product.id).in_(product_ids))
        )
        results = await self.session.exec(statement=statement)
        products = results.all()
        return [ProductForOrder(**product.model_dump()) for product in products]


    async def update(self, product: ProductOut) -> None:
        # todo: implement
        statement = select(Product).where(Product.id == product.id)
        results = await self.session.exec(statement=statement)
        product_to_update = results.one()

    async def get_price_range(self, subdomain: str) -> PriceRange:
        statement = (
            select(
                func.min(Product.price).label("minimum"),
                func.max(Product.price).label("maximum"),
            )
            .join(Storefront, Product.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        results = await self.session.exec(statement)
        min_price, max_price = results.one()
        return PriceRange(minimum=min_price, maximum=max_price)

    async def get_medium_counts(self, subdomain: str) -> list[MediumCount]:
        statement = (
            select(Medium.id, Medium.name, func.count(Product.medium_id).label("count"))
            .select_from(Medium)
            .join(Product, Medium.id == Product.medium_id, isouter=True)
            .join(Storefront, Product.storefront_id == Storefront.id, isouter=True)
            .where(Storefront.subdomain == subdomain)
            .group_by(Medium.id, Medium.name)
        )
        results = await self.session.exec(statement)
        medium_counts = results.all()
        return [
            MediumCount(id=medium_count[0], name=medium_count[1], count=medium_count[2])
            for medium_count in medium_counts
        ]

    async def get_size_ranges(self, subdomain: str) -> SizeRanges:
        statement = (
            select(
                func.min(Product.width).label("width_minimum"),
                func.max(Product.width).label("width_maximum"),
                func.min(Product.height).label("height_minimum"),
                func.max(Product.height).label("height_maximum"),
            )
            .join(Storefront, Product.storefront_id == Storefront.id)
            .where(Storefront.subdomain == subdomain)
        )
        results = await self.session.exec(statement)
        width_minimum, width_maximum, height_minimum, height_maximum = results.one()
        return SizeRanges(
            width_minimum=width_minimum,
            width_maximum=width_maximum,
            height_minimum=height_minimum,
            height_maximum=height_maximum,
        )

    @staticmethod
    def apply_query_params(statement: Select, query_params: ProductQueryParams | None) -> Select:
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
                statement = statement
        return statement

