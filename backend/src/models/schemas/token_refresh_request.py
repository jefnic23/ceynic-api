from backend.src.database import BaseSchema


class TokenRefreshRequest(BaseSchema):
    refresh_token: str
