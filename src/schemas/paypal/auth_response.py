from src.database import BaseSchema


class AuthResponse(BaseSchema):
    scope: str
    access_token: str
    token_type: str
    app_id: str
    expires_in: int
    nonce: str
