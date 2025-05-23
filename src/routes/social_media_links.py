from typing import Annotated
from fastapi import APIRouter, Depends, Response

from src.dependencies import STOREFRONT_ID_DEPENDENCY
from src.models.social_media_link import SocialMediaLinkOut
from src.repositories.social_media_link_repository import SocialMediaLinkRepository

router = APIRouter()


@router.get("/socialMediaLinks")
async def get_social_media_links(
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    social_media_link_repository: Annotated[SocialMediaLinkRepository, Depends()],
    response: Response
) -> list[SocialMediaLinkOut]:
    social_media_links = await social_media_link_repository.get_all(storefront_id)
    response.headers["cache-control"] = "max-age=3600"
    return social_media_links
