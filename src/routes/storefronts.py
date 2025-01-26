from fastapi import APIRouter

from src.dependencies import SUBDOMAIN_DEPENDENCY, STOREFRONTS_SERVICE_DEPENDENCY
from src.models.schemas.location import Location

router = APIRouter()


@router.get("/storefronts/location")
async def get_location(
    subdomain: SUBDOMAIN_DEPENDENCY, 
    storefronts_service: STOREFRONTS_SERVICE_DEPENDENCY
) -> Location:
    return await storefronts_service.get_locations(subdomain)
