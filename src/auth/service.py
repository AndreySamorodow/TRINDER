from fastapi import HTTPException, Response

from src.auth.dependencies import create_access_token, get_password_hash
from src.auth.repository import UserRepository
from src.auth.shemas import UserCreate, UserLogin

from src.database.dao import UserDao


class UserService:
    def __init__(self, db):
        self.db = db
        self.user_repository = UserRepository(db)
        self.dao = UserDao()

    async def register(self, user_data: UserCreate):
        await self.user_repository.verify_reg_data(user_data)

        hashed_password = get_password_hash(user_data.password)
        await self.dao.add(db=self.db, email=user_data.email, password=hashed_password)
        raise HTTPException(status_code=200)

    async def login(self, user_data: UserLogin, response: Response):
        user = await self.user_repository.verify_login_data(user_data)
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("TRINDER_ACCESS_TOKEN", access_token, httponly=True)
        return user

