from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import RedirectResponse

from src.core.redis import RedisSession
from src.profile.dependencies import parse_profile_create
from src.profile.schemas import ProfileCreate, ProfileResponse, TelegramBindSchema
from src.dependencies.user import UserId
from src.profile.service import ProfileService
from src.database.database import DbSession


router = APIRouter(prefix="/api/profile", tags=["Profile"])

# просмотр моего профиля
@router.get("")
async def get_profile(db: DbSession, user_id: UserId) -> ProfileResponse:
    service = ProfileService(db)
    return await service.get_profile(user_id)

# просмотр профиля по ID
@router.get("/{user_id}")
async def get_profile_by_id(user_id: int, db: DbSession) -> ProfileResponse:
    service = ProfileService(db)
    return await service.get_profile(user_id)

# изменить профиль
@router.post("/create")
async def create_profile(
        user_id: UserId,
        db: DbSession,
        user_data: ProfileCreate = Depends(parse_profile_create),
        photo: Optional[UploadFile] = File(None)
    ) -> ProfileResponse:
    service = ProfileService(db)
    return await service.create_or_change_profile(user_id, user_data, photo)

# редирект в телеграм для аутентификации
@router.post("/link_tg")
async def link_an_tg(
    user_id: UserId,
    db: DbSession,
    redis: RedisSession
):
    service = ProfileService(db)
    url = await service.get_link_tg_url(user_id, redis)
    print(url)
    return RedirectResponse(url)

@router.post("/auth/telegram-bind")
async def bind_telegram_account(
    data: TelegramBindSchema,
    db: DbSession,
    redis: RedisSession
    ):
    service = ProfileService(db)
    return await service.bind_tg_account(data, redis)
