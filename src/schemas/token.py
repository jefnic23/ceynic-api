from src.decorators import frontend
from src.schemas.base import BaseSchema


@frontend
class Token(BaseSchema):
    access_token: str
    token_type: str
    refresh_token: str
