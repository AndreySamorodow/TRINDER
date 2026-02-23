from fastapi import HTTPException, status

from src.auth.shemas import UserCreate
from src.database.dao import UserDao


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def verify_reg_data(self, user_data: UserCreate):
        verify_email = await UserDao.find_one_or_none(self.db, email=user_data.email)

        if verify_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email address already exists")
        if user_data.password != user_data.password_replay:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password repetition")
