from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.core.redis import RedisSession
from src.profile.preference.schemas import PreferenceCreate, PreferenceResponse
from src.profile.preference.service import PreferenceService
from src.dependencies.user import UserId
from src.database.database import DbSession


router = APIRouter(prefix="/api/preference", tags=["Preference"])

#просмотр предпочтений
@router.get("/")
async def get_my_preference(db: DbSession, user_id:UserId) -> PreferenceResponse:
    service = PreferenceService(db)
    return await service.get_preference(user_id)


@router.get("/{user_id}")
@cache(expire=60)
async def get_preference_by_id(user_id: int, db: DbSession) -> PreferenceResponse:
    service = PreferenceService(db)
    return await service.get_preference(user_id)


# изменить профиль
@router.post("/create")
async def create_preference(
    user_id: UserId,
    db: DbSession,
    redis: RedisSession,
    user_data: PreferenceCreate
    ) -> PreferenceResponse:
    service = PreferenceService(db)
    return await service.create_or_change_preference(redis, user_id, user_data)
