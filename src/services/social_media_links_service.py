from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.models.social_media_link import SocialMediaLink, SocialMediaLinkOut


class SocialMediaLinksService:
    def __init__(
        self,
        session: ASYNC_SESSION_DEPENDENCY
    ):
        self._session = session

    async def get_all(self, storefront_id: int) -> list[SocialMediaLinkOut]:
        statement = select(SocialMediaLink).where(SocialMediaLink.storefront_id == storefront_id)
        results = await self._session.exec(statement=statement)
        return results.all()