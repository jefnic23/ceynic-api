from decimal import Decimal
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        ser_json_encoders={Decimal: lambda v: str(v)}
    )
