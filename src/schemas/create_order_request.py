from src.database import BaseSchema


class CreateOrderRequest(BaseSchema):
    product_ids: list[int]
