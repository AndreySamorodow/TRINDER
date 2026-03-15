from fastapi import APIRouter, Response

from src.profile.schemas import ProfileResponseList
from src.dependencies.swipe import LastProfileId
from src.database.database import DbSession
from src.dependencies.user import UserId
from src.swipe.service import SwipeService


router = APIRouter(prefix="/api/swipe", tags=["Swipe"])

#получить колоду анкет
@router.get("/get_profiles")
async def picker(
    response: Response,
    user_id: UserId,
    db:DbSession,
    last_profile_id: LastProfileId
) -> ProfileResponseList:
    service = SwipeService(db)
    return await service.get_profiles(response, user_id, last_profile_id)

@router.post("/{swipe_id}")
async def swipe(
    user_id: UserId,
    swipe_id: int,
    db:DbSession,
):
    service = SwipeService(db)
    return await service.swipe(user_id, swipe_id)

