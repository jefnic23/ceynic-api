from pydantic import ConfigDict, Field

from src.schemas.base import BaseSchema


class PayPalCredentials(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    client_id: str = Field(min_length=1)
    client_secret: str = Field(min_length=1)
