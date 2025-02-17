from pydantic import BaseModel
from typing import Optional

from src.models.enums.product_sort_params import ProductSortParams

class ProductQueryParams(BaseModel):
    sort: Optional[ProductSortParams] = None
    mediums: Optional[list[str]] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
