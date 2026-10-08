from typing import Annotated
from fastapi import APIRouter, Depends, Response

from src.dependencies import STOREFRONT_ID_DEPENDENCY
from src.models.social_media_link import SocialMediaLinkOut
from src.services.social_media_links_service import SocialMediaLinksService

router = APIRouter()


@router.get("/socialMediaLinks")
async def get_social_media_links(
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    social_media_links_service: Annotated[SocialMediaLinksService, Depends()],
    response: Response
) -> list[SocialMediaLinkOut]:
    social_media_links = await social_media_links_service.get_all(storefront_id)
    response.headers["cache-control"] = "max-age=3600"
    return social_media_links
