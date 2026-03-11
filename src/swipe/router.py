from fastapi import APIRouter

from src.database.database import DbSession
from src.dependencies.user import UserId
from src.swipe.picker import SwipeService


router = APIRouter(prefix="/api/swipe", tags=["Swipe"])

@router.get("/get_profiles")
async def picker(user_id: UserId, db:DbSession):
    service = SwipeService(db)
    return await service.get_profiles(user_id, 10)