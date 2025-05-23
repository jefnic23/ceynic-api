from decimal import Decimal
from src.schemas.base import BaseSchema


class PriceRange(BaseSchema):
    minimum: Decimal
    maximum: Decimal


class MediumCount(BaseSchema):
    id: int
    name: str
    count: int


class SizeRanges(BaseSchema):
    width_minimum: int
    width_maximum: int
    height_minimum: int
    height_maximum: int


class ProductMetadata(BaseSchema):
    price_range: PriceRange
    medium_counts: list[MediumCount]
    size_ranges: SizeRanges
