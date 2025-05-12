from fastapi import APIRouter, Response
from src.dependencies import SOCIAL_MEDIA_LINK_REPOSITORY_DEPENDENCY, STOREFRONT_ID_DEPENDENCY
from src.models.schemas.social_media_link_out import SocialMediaLinkOut

router = APIRouter()


@router.get("/socialMediaLinks")
async def get_social_media_links(
    storefront_id: STOREFRONT_ID_DEPENDENCY,
    social_media_link_repository: SOCIAL_MEDIA_LINK_REPOSITORY_DEPENDENCY,
    response: Response
) -> list[SocialMediaLinkOut]:
    social_media_links = await social_media_link_repository.get_all(storefront_id)
    response.headers["cache-control"] = "max-age=3600"
    return social_media_links
