from src.auth.dependencies import get_password_hash
from src.auth.repository import UserRepository
from src.auth.shemas import UserCreate


class UserService:
    def __init__(self, db):
        self.db = db
        self.user_repository = UserRepository(db)

    async def register(self, user_data: UserCreate):
        await self.user_repository.verify_reg_data(user_data)

        hashed_password = get_password_hash(user_data.password)
        

