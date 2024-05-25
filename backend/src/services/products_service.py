from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.config import Settings
from backend.src.models.product import Product
from backend.src.models.schemas.product import ProductOut, ProductsOut
from backend.src.services.aws_service import AwsService


class ProductsService:
    def __init__(self, session: AsyncSession, settings: Settings, aws: AwsService):
        self.session = session
        self.settings = settings
        self.aws = aws

    async def get_all(self) -> list[ProductsOut]:
        statement = select(Product)
        results = await self.session.exec(statement=statement)
        products = results.all()
        return [
            ProductsOut(
                **product.model_dump(),
                image_url=f"https://{self.settings.BUCKETEER_BUCKET_NAME}.s3.amazonaws.com/public/{product.title.replace(' ', '_')}/{product.thumbnail}",
            )
            for product in products
        ]

    async def get(self, id: int) -> ProductOut:
        statement = select(Product).where(Product.id == id)
        results = await self.session.exec(statement=statement)
        product = results.first()
        images = await self.aws.get_product_images(product.title)
        return ProductOut(
            **product.model_dump(),
            images=images,
        )
