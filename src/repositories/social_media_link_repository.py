from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_async_session
from src.models.social_media_link import SocialMediaLink, SocialMediaLinkOut


class SocialMediaLinkRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self._session: AsyncSession = session

    async def get_all(self, storefront_id: int) -> list[SocialMediaLinkOut]:
        statement = select(SocialMediaLink).where(SocialMediaLink.storefront_id == storefront_id)
        results = await self._session.exec(statement=statement)
        return results.all()
