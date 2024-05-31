from typing import Annotated, AsyncGenerator

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.src.config import SETTINGS_DEPENDENCY, Settings
from backend.src.models.medium import Medium  # noqa: F401
from backend.src.models.order import Order  # noqa: F401
from backend.src.models.product import Product  # noqa: F401
from backend.src.models.user import User  # noqa: F401


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Database:
    def __init__(self, settings: Settings):
        self.engine: AsyncEngine = create_async_engine(
            settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://"),
            echo=False,
            future=True,
        )
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )


async def get_database(
    settings: SETTINGS_DEPENDENCY,
) -> Database:
    return Database(settings=settings)


DATABASE_DEPENDENCY = Annotated[Database, Depends(get_database)]


async def get_async_session(
    database: DATABASE_DEPENDENCY,
) -> AsyncGenerator[AsyncSession, None]:
    async with database.async_session() as async_session:
        yield async_session


ASYNC_SESSION_DEPENDENCY = Annotated[AsyncSession, Depends(get_async_session)]
