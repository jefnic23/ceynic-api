from enum import Enum


class PaymentProcessorEnum(Enum):
    PAYPAL = "PayPal"
    STRIPE = "Stripe"
