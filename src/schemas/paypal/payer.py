from pydantic import EmailStr
from src.schemas.base import BaseSchema
from src.schemas.paypal.base import Name


class Payer(BaseSchema):
    name: Name
    email_address: EmailStr
    payer_id: str
