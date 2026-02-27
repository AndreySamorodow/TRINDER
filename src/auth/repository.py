from fastapi import HTTPException, status

from src.auth.dependencies import verify_password
from src.auth.shemas import UserCreate, UserLogin
from src.database.dao import UserDao


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def verify_reg_data(self, user_data: UserCreate):
        user = await UserDao.find_one_or_none(self.db, email=user_data.email)

        if user:
            if not user.oauth:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email address already exists")
            
        if user_data.password != user_data.password_replay:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password repetition")


    async def verify_login_data(self, user_data: UserLogin):
        user = await UserDao.find_one_or_none(self.db, email=user_data.email)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There is no user with this email address")
        
        if not user.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can only sign in to your account through Google, or register again.")

        if not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password is incorrect")
        
        return user

