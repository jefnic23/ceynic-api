from pydantic import BaseModel
from src.schemas.paypal.purchase_unit import PurchaseUnit


class CreateOrderPayload(BaseModel):
    intent: str = "AUTHORIZE"
    purchase_units: list[PurchaseUnit]
