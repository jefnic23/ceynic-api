from datetime import datetime

from pydantic import BaseModel


class ReCaptchaResponse(BaseModel):
    success: bool
    challenge_ts: datetime
    hostname: str
    score: float | None
    action: str | None
    error_codes: list[str] | None = None
