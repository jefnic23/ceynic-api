from src.database import BaseSchema

class SizeRanges(BaseSchema):
    width_minimum: int
    width_maximum: int
    height_minimum: int
    height_maximum: int
