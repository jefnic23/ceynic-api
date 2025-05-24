from src.decorators import frontend
from src.schemas.base import BaseSchema


@frontend
class Location(BaseSchema):
    city: str | None
    state: str
