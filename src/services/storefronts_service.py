from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.schemas.location import Location
from src.models.storefront import Storefront

class StorefrontsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_locations(self, subdomain: str) -> Location:
        statement = select(Storefront).where(Storefront.name == subdomain)
        result = await self.session.exec(statement)
        storefront = result.one()
        return Location(city=storefront.city, state=storefront.state)