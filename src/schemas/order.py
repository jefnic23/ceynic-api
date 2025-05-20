from datetime import datetime
from src.database import BaseSchema


class OrdersOut(BaseSchema):
    id: str
    create_time: datetime
    status: str
