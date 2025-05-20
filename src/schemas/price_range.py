from decimal import Decimal
from src.database import BaseSchema

class PriceRange(BaseSchema):
    minimum: Decimal
    maximum: Decimal
