from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    product_id: int
