from pydantic import ConfigDict

from src.decorators import frontend
from src.schemas.base import BaseSchema


@frontend
class SiteSettings(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    pinterest_enabled: bool = False
    sort_and_filter_enabled: bool = True
