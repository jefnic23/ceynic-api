from src.enums.payment_processor import PaymentProcessorEnum
from src.schemas.base import BaseSchema


class PaymentProcessorSelection(BaseSchema):
    processor: PaymentProcessorEnum


class ConfiguredPaymentProcessors(BaseSchema):
    processors: list[PaymentProcessorEnum]
