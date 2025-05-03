from src.database import BaseSchema

class PayPalCredentials(BaseSchema):
    client_id: str
    client_secret: str
