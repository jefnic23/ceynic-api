from typing import Annotated
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_async_session
from src.models.storefront import Storefront
from src.models.user import User


class UsersService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_async_session)]):
        self._session = session

    async def get_user_by_id(self, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        result = await self._session.exec(statement=statement)
        return result.one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self._session.exec(statement=statement)
        return result.one_or_none()

    async def get_subdomain_from_user(self, id: int) -> str | None:
        statement = (
            select(Storefront.subdomain)
            .join(User, User.storefront_id == Storefront.id)
            .where(User.id == id)
        )
        result = await self._session.exec(statement=statement)
        return result.one_or_none()
