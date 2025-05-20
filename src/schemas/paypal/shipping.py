from src.database import BaseSchema
from src.schemas.paypal.base import Address


class Shipping(BaseSchema):
    address: Address