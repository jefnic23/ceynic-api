from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

from src.schemas.site_settings import SiteSettings


class SiteSettingsType(TypeDecorator[SiteSettings]):
    """Store a validated SiteSettings model as PostgreSQL JSONB."""

    impl = JSONB
    cache_ok = True

    def process_bind_param(self, value: SiteSettings | dict[str, Any], dialect: Dialect) -> dict[str, Any]:
        return SiteSettings.model_validate(value).model_dump(mode="json", by_alias=False)

    def process_result_value(self, value: dict[str, Any], dialect: Dialect) -> SiteSettings:
        return SiteSettings.model_validate(value)
