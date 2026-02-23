from fastapi import APIRouter

from src.auth.service import UserService
from src.database.database import DbSession
from src.auth.shemas import UserCreate


router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
async def register(user_data: UserCreate, db: DbSession):
    service = UserService(db)
    return await service.register(user_data)
