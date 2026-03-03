from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.auth.models import User
from src.database.dao import UserDao


class ProfileRepository:
    def __init__(self, db):
        self.db = db
        self.user_dao = UserDao()
    
    async def get_profile_by_id(self, user_id):
        query = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.profile))
        )
        result = await self.db.execute(query)
        user = result.unique().scalar_one_or_none()
        return user.profile if user else None
    
    async def create_profile(self, profile):
        try:
            self.db.add(profile)
            await self.db.commit()  
            await self.db.refresh(profile)
            return profile
                
        except Exception as e:
            await self.db.rollback()
            raise e
