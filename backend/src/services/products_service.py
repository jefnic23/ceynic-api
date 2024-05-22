from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.models.product import Product


class ProductsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Product]:
        statement = select(Product)
        results = await self.session.exec(statement=statement)
        return results.all()

    async def get(self, id: int) -> Product:
        statement = select(Product).where(Product.id == id)
        results = await self.session.exec(statement=statement)
        return results.first()
