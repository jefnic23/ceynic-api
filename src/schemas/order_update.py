from datetime import datetime
from src.database import BaseSchema


class OrderUpdate(BaseSchema):
    authorization_id: str | None = None
    capture_id: str | None = None
    status: str | None = None
