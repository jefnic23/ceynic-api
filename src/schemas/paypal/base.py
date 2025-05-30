from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, EmailStr


class Address(BaseModel):
    address_line_1: str | None = None
    address_line_2: str | None = None
    admin_area_2: str | None = None
    admin_area_1: str | None = None
    postal_code: str | None = None
    country_code: str | None = None


class GrossAmount(BaseModel):
    currency_code: str
    value: Decimal


class Link(BaseModel):
    href: str
    rel: str
    method: str


class Name(BaseModel):
    given_name: str | None = None
    surname: str | None = None


class NetAmount(BaseModel):
    currency_code: str
    value: Decimal


class Payee(BaseModel):
    email_address: EmailStr
    merchant_id: str


class PaypalFee(BaseModel):
    currency_code: str
    value: Decimal


class Phone(BaseModel):
    country_code: str
    national_number: str
    phone_type: Literal["MOBILE", "HOME", "WORK", "OTHER"]


class SellerProtection(BaseModel):
    status: str
    dispute_categories: list[str]


class UnitAmount(BaseModel):
    currency_code: str = "USD"
    value: str


class Breakdown(BaseModel):
    item_total: UnitAmount
    shipping: UnitAmount | None = None


class Amount(BaseModel):
    currency_code: str = "USD"
    value: str
    breakdown: Breakdown


class Tax(BaseModel):
    name: str
    percent: str
    tax_note: str | None = None
