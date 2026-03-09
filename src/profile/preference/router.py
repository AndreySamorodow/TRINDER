from fastapi import APIRouter

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
async def get_my_preference(user_id: int, db: DbSession) -> PreferenceResponse:
    service = PreferenceService(db)
    return await service.get_preference(user_id)


# изменить профиль
@router.post("/create")
async def create_preference(
    user_id: UserId,
    db: DbSession,
    user_data: PreferenceCreate
    ) -> PreferenceResponse:
    service = PreferenceService(db)
    return await service.create_or_change_preference(user_id, user_data)
