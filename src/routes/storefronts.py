from typing import Annotated
from fastapi import APIRouter, Depends, Response

from src.dependencies import SUBDOMAIN_DEPENDENCY
from src.schemas.location import Location
from src.services.storefronts_service import StorefrontsService

router = APIRouter()


@router.get("/storefronts/location")
async def get_location(
    subdomain: SUBDOMAIN_DEPENDENCY, 
    storefronts_service: Annotated[StorefrontsService, Depends()],
    response: Response
) -> Location:
    response.headers["cache-control"] = "max-age=3600"
    return await storefronts_service.get_locations(subdomain)

@router.get("/storefronts/about")
async def get_about(
    subdomain: SUBDOMAIN_DEPENDENCY,
    storefronts_service: Annotated[StorefrontsService, Depends()],
    response: Response
) -> str:
    response.headers["cache-control"] = "max-age=3600"
    return await storefronts_service.get_about(subdomain)

@router.get("/storefronts/name")
async def get_about(
    subdomain: SUBDOMAIN_DEPENDENCY,
    storefronts_service: Annotated[StorefrontsService, Depends()],
    response: Response
) -> str:
    response.headers["cache-control"] = "max-age=3600"
    return await storefronts_service.get_name(subdomain)
