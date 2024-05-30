from pydantic import BaseModel


class PayPalAuthResponse(BaseModel):
    scope: str
    access_token: str
    token_type: str
    app_id: str
    expires_in: int
    nonce: str
