from fastapi import APIRouter, Depends, File, UploadFile

from src.profile.dependencies import parse_profile_create
from src.profile.schemas import ProfileCreate
from src.dependencies.user import UserId
from src.profile.service import ProfileService
from src.database.database import DbSession


router = APIRouter(prefix="/profile", tags=["Profile"])

# просмотр моего профиля
@router.get("")
async def get_profile(db: DbSession, user_id: UserId):
    service = ProfileService(db)
    return await service.get_profile(user_id)

# просмотр профиля по ID
@router.get("/{user_id}")
async def get_profile_by_id(user_id: int, db: DbSession):
    service = ProfileService(db)
    return await service.get_profile(user_id)

# изменить профиль
@router.post("/create")
async def create_profile(
    user_id: UserId,
    db: DbSession,
    user_data: ProfileCreate = Depends(parse_profile_create),
    photo: UploadFile = File(...)
    ):
    service = ProfileService(db)
    return await service.create_or_change_profile(user_id, user_data, photo)
