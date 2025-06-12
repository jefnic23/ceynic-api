from pydantic import EmailStr
from src.schemas.base import BaseSchema
from src.schemas.paypal.base import Address, Name


class Paypal(BaseSchema):
    name: Name
    email_address: EmailStr | None = None
    account_id: str | None = None
    account_status: str | None = None
    address: Address | None = None
