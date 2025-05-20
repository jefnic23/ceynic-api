from src.database import BaseSchema
from src.schemas.paypal.purchase_unit import PurchaseUnit


class CreateOrderPayload(BaseSchema):
    intent: str = "AUTHORIZE"
    purchase_units: list[PurchaseUnit]
