from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import ASYNC_SESSION_DEPENDENCY
from src.models.refresh_token import RefreshToken


class RefreshTokensService:
    def __init__(self, session: ASYNC_SESSION_DEPENDENCY):
        self._session = session

    async def get_refresh_token(self, user_id: int) -> RefreshToken | None:
        statement = select(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self._session.exec(statement=statement)
        return result.one_or_none()
