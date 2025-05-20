from src.database import BaseSchema


class SocialMediaLinkOut(BaseSchema):
    name: str
    url: str
