from fastapi import APIRouter

from src.dependencies import CURRENT_USER_DEPENDENCY
from src.schemas.user_out import UserOut

router = APIRouter()


@router.get("/users")
async def get_user(current_user: CURRENT_USER_DEPENDENCY) -> UserOut:
    return UserOut.model_validate(current_user)
