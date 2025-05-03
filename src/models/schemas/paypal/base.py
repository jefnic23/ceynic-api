from decimal import Decimal
from typing import Literal

from pydantic import EmailStr
from src.database import BaseSchema


class Address(BaseSchema):
    address_line_1: str | None = None
    address_line_2: str | None = None
    admin_area_2: str | None = None
    admin_area_1: str | None = None
    postal_code: str | None = None
    country_code: str | None = None


class Amount(BaseSchema):
    currency_code: str = "USD"
    value: Decimal


class GrossAmount(BaseSchema):
    currency_code: str
    value: Decimal


class Link(BaseSchema):
    href: str
    rel: str
    method: str


class Name(BaseSchema):
    given_name: str | None = None
    surname: str | None = None


class NetAmount(BaseSchema):
    currency_code: str
    value: Decimal


class Payee(BaseSchema):
    email_address: EmailStr
    merchant_id: str


class PaypalFee(BaseSchema):
    currency_code: str
    value: Decimal


class Phone(BaseSchema):
    country_code: str
    national_number: str
    phone_type: Literal["MOBILE", "HOME", "WORK", "OTHER"]


class SellerProtection(BaseSchema):
    status: str
    dispute_categories: list[str]


class UnitAmount(BaseSchema):
    currency_code: str
    value: str


class Tax(BaseSchema):
    name: str
    percent: str
    tax_note: str | None = None
