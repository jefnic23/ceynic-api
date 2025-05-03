from src.database import BaseSchema
from src.models.schemas.paypal.purchase_unit import PurchaseUnit


class CreateOrderPayload(BaseSchema):
    intent: str = "AUTHORIZE"
    purchase_units: list[PurchaseUnit]
