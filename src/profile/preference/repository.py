


from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.profile.preference.schemas import PreferenceResponse
from src.auth.models import User


class PreferenceRepository:
    def __init__(self, db):
        self.db = db

    async def get_preference_by_id(self, user_id: int):
        query = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.profile), joinedload(User.preference))
        )
        result = await self.db.execute(query)
        user = result.unique().scalar_one_or_none()
        return user.preference if user else None
    

    async def create_preference(self, preference) -> PreferenceResponse:
        try:
            self.db.add(preference)
            await self.db.commit()  
            await self.db.refresh(preference)
            return PreferenceResponse.model_validate(preference)
                
        except Exception as e:
            await self.db.rollback()
            raise e
        