from src.database import BaseSchema

class Location(BaseSchema):
    city: str | None
    state: str
