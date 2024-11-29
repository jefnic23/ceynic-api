from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Settings
from src.models.enums.product_sort_params import ProductSortParams
from src.models.product import Product
from src.models.schemas.product import ProductOut, ProductsOut
from src.services.aws_service import AwsService


class ProductsService:
    def __init__(self, session: AsyncSession, settings: Settings, aws: AwsService):
        self.session = session
        self.settings = settings
        self.aws = aws

    async def get_all(self, sort: ProductSortParams | None = None) -> list[ProductsOut]:
        statement = select(Product)
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
            else:
                statement = statement.order_by(
                    Product.height.desc(), Product.width.desc()
                )
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

    async def get(self, product_id: int) -> ProductOut:
        statement = select(Product).where(Product.id == product_id)
        results = await self.session.exec(statement=statement)
        product = results.first()
        images = await self.aws.get_product_images(product.title)
        return ProductOut(
            **product.model_dump(),
            images=images,
        )
