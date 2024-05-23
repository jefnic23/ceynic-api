from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.models.product import Product
from backend.src.models.schemas.product import ProductOut, ProductsOut
from backend.src.services.aws_service import AwsService


class ProductsService:
    def __init__(self, session: AsyncSession, aws: AwsService):
        self.session = session
        self.aws = aws

    async def get_all(self) -> list[ProductsOut]:
        statement = select(
            Product.id,
            Product.title,
            Product.price,
            Product.height,
            Product.width,
            Product.thumbnail,
        )
        results = await self.session.exec(statement=statement)
        products = results.all()
        return [
            ProductsOut(
                id=product.id,
                title=product.title,
                price=product.price,
                height=product.height,
                width=product.width,
                thumbnail=product.thumbnail,
            )
            for product in products
        ]

    async def get(self, id: int) -> ProductOut:
        statement = select(
            Product.id,
            Product.title,
            Product.price,
            Product.height,
            Product.width,
            Product.thumbnail,
            Product.description,
            Product.slideshow,
        ).where(Product.id == id)
        results = await self.session.exec(statement=statement)
        product = results.first()
        images = await self.aws.get_product_images(product.title.replace(" ", "_"))
        return ProductOut(
            id=product.id,
            title=product.title,
            price=product.price,
            height=product.height,
            width=product.width,
            thumbnail=product.thumbnail,
            description=product.description,
            slideshow=product.slideshow,
            images=images,
        )
