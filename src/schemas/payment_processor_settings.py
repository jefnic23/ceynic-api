from typing import Any

from pydantic import ConfigDict, Field, field_validator

from src.enums.payment_processor import PaymentProcessorEnum
from src.schemas.base import BaseSchema
from src.schemas.paypal_credentials import PayPalCredentials


# Register a credentials schema here when adding a new payment processor.
PROCESSOR_CREDENTIALS: dict[str, type[BaseSchema]] = {
    PaymentProcessorEnum.PAYPAL.value: PayPalCredentials,
}


class PaymentProcessorSettings(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    # The active processor is selected by settings.payment_processor, not by this map.
    processors: dict[str, dict[str, Any]] = Field(default_factory=dict)

    @field_validator("processors")
    @classmethod
    def validate_processors(cls, processors: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        validated = {}
        for name, credentials in processors.items():
            schema = PROCESSOR_CREDENTIALS.get(name)
            if schema is None:
                raise ValueError(f"Unsupported payment processor: {name}")
            validated[name] = schema.model_validate(credentials).model_dump(mode="json", by_alias=False)
        return validated
