from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.schemas.social_media_link_out import SocialMediaLinkOut
from src.models.social_media_link import SocialMediaLink


class SocialMediaLinkRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def get_all(self, storefront_id: int) -> list[SocialMediaLinkOut]:
        statement = select(SocialMediaLink).where(SocialMediaLink.storefront_id == storefront_id)
        results = await self._session.exec(statement=statement)
        return [SocialMediaLinkOut(**social_media_link.model_dump()) for social_media_link in results.all()]
