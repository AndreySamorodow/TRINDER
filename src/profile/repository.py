import json
from typing import List

from sqlalchemy import select

from src.profile.models import Profile
from src.profile.schemas import ProfileResponse
from src.database.dao import UserDao


class ProfileRepository:
    def __init__(self, db):
        self.db = db
        self.user_dao = UserDao()
    
    async def get_profile_by_id(self, user_id: int) -> Profile | None:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_profiles_by_ids(self, profile_ids: List[int]) -> List[Profile]:
        if not profile_ids:
            return []
        stmt = select(Profile).where(Profile.id.in_(profile_ids))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def create_profile(self, profile) -> ProfileResponse:
        try:
            self.db.add(profile)
            await self.db.commit()  
            await self.db.refresh(profile)
            return ProfileResponse.model_validate(profile)
                
        except Exception as e:
            await self.db.rollback()
            raise e


    async def rebuild_user_deck(self, user_id: int, redis):
        from src.swipe.deck_builder import DeckBuilder

        builder = DeckBuilder(self.db)
        deck = await builder.build_for_user(user_id)
        key = f"deck:{user_id}"
        if deck:
            await redis.setex(key, 86400, json.dumps(deck))
        else:
            await redis.delete(key)
