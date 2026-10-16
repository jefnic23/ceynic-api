from pydantic import BaseModel

from src.enums.product_sort_params import ProductSortParams


class ProductQueryParams(BaseModel):
    sort: ProductSortParams | None = None
    medium: list[str] | None = None
    min_price: int | None = None
    max_price: int | None = None
    min_width: int | None = None
    max_width: int | None = None
    min_height: int | None = None
    max_height: int | None = None
    sold: bool = False
