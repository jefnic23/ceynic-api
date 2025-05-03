from fastapi import APIRouter, Response

from src.dependencies import SUBDOMAIN_DEPENDENCY, STOREFRONTS_SERVICE_DEPENDENCY
from src.models.schemas.location import Location

router = APIRouter()


@router.get("/storefronts/location")
async def get_location(
    subdomain: SUBDOMAIN_DEPENDENCY, 
    storefronts_service: STOREFRONTS_SERVICE_DEPENDENCY,
    response: Response
) -> Location:
    response.headers["cache-control"] = "max-age=3600"
    return await storefronts_service.get_locations(subdomain)

@router.get("/storefronts/about")
async def get_about(
    subdomain: SUBDOMAIN_DEPENDENCY,
    storefronts_service: STOREFRONTS_SERVICE_DEPENDENCY,
    response: Response
) -> str:
    response.headers["cache-control"] = "max-age=3600"
    return await storefronts_service.get_about(subdomain)

@router.get("/storefronts/name")
async def get_about(
    subdomain: SUBDOMAIN_DEPENDENCY,
    storefronts_service: STOREFRONTS_SERVICE_DEPENDENCY,
    response: Response
) -> str:
    response.headers["cache-control"] = "max-age=3600"
    return await storefronts_service.get_name(subdomain)
