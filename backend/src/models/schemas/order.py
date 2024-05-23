from pydantic import BaseModel


class Name(BaseModel):
    given_name: str
    surname: str


class Paypal(BaseModel):
    name: Name
    email_address: str
    account_id: str


class PaymentSource(BaseModel):
    paypal: Paypal


class Address(BaseModel):
    address_line_1: str
    address_line_2: str | None
    admin_area_2: str
    admin_area_1: str
    postal_code: str
    country_code: str


class Shipping(BaseModel):
    address: Address


class Amount(BaseModel):
    currency_code: str
    value: str


class GrossAmount(BaseModel):
    currency_code: str
    value: str


class PaypalFee(BaseModel):
    currency_code: str
    value: str


class NetAmount(BaseModel):
    currency_code: str
    value: str


class SellerReceivableBreakdown(BaseModel):
    gross_amount: GrossAmount
    paypal_fee: PaypalFee
    net_amount: NetAmount


class Link(BaseModel):
    href: str
    rel: str
    method: str


class Capture(BaseModel):
    id: str
    status: str
    amount: Amount
    seller_protection: dict
    final_capture: bool
    disbursement_mode: str
    seller_receivable_breakdown: SellerReceivableBreakdown
    create_time: str
    update_time: str
    links: list[Link]


class Payments(BaseModel):
    captures: list[Capture]


class PurchaseUnit(BaseModel):
    reference_id: str
    shipping: Shipping
    payments: Payments


class Payer(BaseModel):
    name: Name
    email_address: str
    payer_id: str


class Order(BaseModel):
    id: str
    status: str
    payment_source: PaymentSource
    purchase_units: list[PurchaseUnit]
    payer: Payer
    links: list[Link]
