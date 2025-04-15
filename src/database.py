
from typing import Annotated, AsyncGenerator, AsyncIterator

from fastapi import Depends
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import get_settings
from src.models.content import Content  # noqa: F401
from src.models.medium import Medium  # noqa: F401
from src.models.order import Order  # noqa: F401
from src.models.product import Product  # noqa: F401
from src.models.refresh_token import RefreshToken  # noqa: F401
from src.models.storefront import Storefront  # noqa: F401
from src.models.user import User  # noqa: F401


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Database:
    def __init__(self, database_url: str):
        self._engine: AsyncEngine = create_async_engine(
            database_url.replace("postgres://", "postgresql+asyncpg://"),
            echo=False,
            future=True,
        )
        self._async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self._engine, expire_on_commit=True, class_=AsyncSession
        )

    async def close(self):
        if self._engine is None:
            raise Exception("Database is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._async_session = None

    @asynccontextmanager
    async def async_session(self) -> AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("Database is not initialized")
        async_session = self._async_session()
        try:
            yield async_session
        except Exception:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()

database = Database(get_settings().DATABASE_URL)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.async_session() as async_session:
        yield async_session 


ASYNC_SESSION_DEPENDENCY = Annotated[AsyncSession, Depends(get_async_session)]
