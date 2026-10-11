from sqlalchemy.dialects.postgresql import ENUM

from src.enums.payment_processor import PaymentProcessorEnum


# The migration owns the PostgreSQL type lifecycle; both columns use its labels.
PaymentProcessorType = ENUM(
    *(processor.value for processor in PaymentProcessorEnum if processor.value is not None),
    name="payment_processor",
    create_type=False,
)
