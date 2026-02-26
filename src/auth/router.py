from fastapi import APIRouter, Response

from src.auth.service import UserService
from src.database.database import DbSession
from src.auth.shemas import UserCreate, UserLogin


router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
async def register(user_data: UserCreate, db: DbSession):
    service = UserService(db)
    await service.register(user_data)

@router.post("/login")
async def login(response: Response, user_data: UserLogin, db: DbSession):
    service = UserService(db)
    return await service.login(user_data, response)

