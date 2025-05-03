from src.database import BaseSchema
from src.models.schemas.paypal.base import Address


class Shipping(BaseSchema):
    address: Address