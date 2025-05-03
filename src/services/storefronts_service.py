from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.account_settings import AccountSettings
from src.models.content import Content
from src.models.enums.payment_processor import PaymentProcessorEnum
from src.models.payment_processor import PaymentProcessor
from src.models.schemas.location import Location
from src.models.storefront import Storefront

class StorefrontsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_locations(self, subdomain: str) -> Location:
        statement = select(Storefront).where(Storefront.subdomain == subdomain)
        result = await self.session.exec(statement)
        storefront = result.one()
        return Location(city=storefront.city, state=storefront.state)
    

    async def get_about(self, subdomain: str) -> str:
        statement = select(Content).join(Content.storefront).where(Storefront.subdomain == subdomain)
        result = await self.session.exec(statement)
        content = result.one()
        return content.about
    

    async def get_id_from_subdomain(self, subdomain: str) -> int:
        statement = select(Storefront).where(Storefront.subdomain == subdomain)
        result = await self.session.exec(statement)
        storefront = result.one()
        return storefront.id
    

    async def get_name(self, subdomain: str) -> str:
        statement = select(Storefront).where(Storefront.subdomain == subdomain)
        result = await self.session.exec(statement)
        storefront = result.one()
        return storefront.name
