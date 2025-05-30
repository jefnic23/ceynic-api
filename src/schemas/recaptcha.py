from datetime import datetime

from pydantic import BaseModel


class ReCaptchaResponse(BaseModel):
    success: bool
    challenge_ts: datetime | None = None
    hostname: str | None = None
    score: float | None = None
    action: str | None = None
    error_codes: list[str] | None = None
