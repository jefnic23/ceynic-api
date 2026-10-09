from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlmodel import Field, Relationship

from src.models.base import BaseModel

if TYPE_CHECKING:
    from src.models.user import User


class RefreshToken(BaseModel, table=True):
    __tablename__ = "refresh_tokens"
    __table_args__ = (UniqueConstraint("user_id", name="uq_refresh_tokens_user_id"),)

    id: int = Field(primary_key=True)
    token: str
    expiry_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    user_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )
    )
    user: "User" = Relationship(back_populates="refresh_token")
