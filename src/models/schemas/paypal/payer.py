from pydantic import EmailStr
from src.database import BaseSchema
from src.models.schemas.paypal.base import Name


class Payer(BaseSchema):
    name: Name
    email_address: EmailStr
    payer_id: str
