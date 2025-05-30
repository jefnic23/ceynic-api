from pydantic import BaseModel
from src.schemas.paypal.base import Address


class Shipping(BaseModel):
    address: Address