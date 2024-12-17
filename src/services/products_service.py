from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.models.enums.product_sort_params import ProductSortParams
from src.models.product import Product
from src.models.schemas.price_range import PriceRange
from src.models.schemas.product import ProductOut, ProductsOut
from src.models.storefront import Storefront
from src.services.aws_service import AwsService


class ProductsService:
    def __init__(self, session: AsyncSession, settings: Settings, aws: AwsService):
        self.session = session
        self.settings = settings
        self.aws = aws

    async def get_all(
        self, subdomain: str, sort: ProductSortParams | None = None
    ) -> list[ProductsOut]:
        statement = (
            select(Product).join(Product.storefront).where(Storefront.name == subdomain)
        )
        if sort:
            if sort == ProductSortParams.OLDEST:
                statement = statement.order_by(Product.date_added)
            elif sort == ProductSortParams.NEWEST:
                statement = statement.order_by(Product.date_added.desc())
            elif sort == ProductSortParams.PRICE_ASC:
                statement = statement.order_by(Product.price)
            elif sort == ProductSortParams.PRICE_DESC:
                statement = statement.order_by(Product.price.desc())
            elif sort == ProductSortParams.SIZE_ASC:
                statement = statement.order_by(Product.height, Product.width)
            elif sort == ProductSortParams.SIZE_DESC:
                statement = statement.order_by(
                    Product.height.desc(), Product.width.desc()
                )
            else:
                statement = statement
        results = await self.session.exec(statement=statement)
        products = results.all()
        # TODO: omit products that don't have any images
        return [
            ProductsOut(
                **product.model_dump(),
                image_url=f"https://{self.settings.BUCKETEER_BUCKET_NAME}.s3.amazonaws.com/public/{product.title.replace(' ', '_')}/{product.thumbnail}",
            )
            for product in products
        ]

    async def get(self, product_id: int, subdomain: str) -> ProductOut:
        statement = (
            select(Product)
            .join(Product.storefront)
            .where(Storefront.name == subdomain)
            .where(Product.id == product_id)
        )
        results = await self.session.exec(statement=statement)
        product = results.one()
        images = await self.aws.get_product_images(product.title)
        return ProductOut(
            **product.model_dump(),
            images=images,
        )

    async def update(self, product: ProductOut) -> None:
        statement = select(Product).where(Product.id == product.id)
        results = await self.session.exec(statement=statement)
        product_to_update = results.one()

    async def get_price_range(self, subdomain: str) -> PriceRange:
        # Select the min and max price values from the Product table, filtered by the Storefront name
        statement = select(
            func.min(Product.price).label("minimum"),
            func.max(Product.price).label("maximum")
        ).join(Product.storefront).where(Storefront.name == subdomain)
        
        # Execute the statement
        results = await self.session.exec(statement)
        
        # Get the result (which will be a tuple of min and max prices)
        min_price, max_price = results.one()
        
        # Return the result as a PriceRange object
        return PriceRange(minimum=min_price, maximum=max_price)

    # todo: static methods for applying sorting/filtering
