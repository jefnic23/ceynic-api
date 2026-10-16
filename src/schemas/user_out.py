from src.schemas.base import BaseSchema


class UserOut(BaseSchema):
    email: str
    first_name: str | None
    last_name: str | None
