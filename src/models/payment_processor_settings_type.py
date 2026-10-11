from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

from src.schemas.payment_processor_settings import PaymentProcessorSettings


class PaymentProcessorSettingsType(TypeDecorator[PaymentProcessorSettings]):
    """Store validated per-processor credentials as PostgreSQL JSONB."""

    impl = JSONB
    cache_ok = True

    def process_bind_param(
        self, value: PaymentProcessorSettings | dict[str, Any], dialect: Dialect
    ) -> dict[str, Any]:
        if isinstance(value, PaymentProcessorSettings):
            value = value.model_dump(mode="json", by_alias=False)
        return PaymentProcessorSettings.model_validate(value).model_dump(mode="json", by_alias=False)

    def process_result_value(
        self, value: dict[str, Any], dialect: Dialect
    ) -> PaymentProcessorSettings:
        return PaymentProcessorSettings.model_validate(value)
