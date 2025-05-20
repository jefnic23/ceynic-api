from enum import Enum


class ProductSortParams(Enum):
    OLDEST = "oldest"
    NEWEST = "newest"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    SIZE_ASC = "size_asc"
    SIZE_DESC = "size_desc"
