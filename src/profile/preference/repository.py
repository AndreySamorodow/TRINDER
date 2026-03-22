from sqlalchemy import select

from src.profile.preference.models import Preference
from src.profile.preference.schemas import PreferenceResponse
from src.auth.models import User


class PreferenceRepository:
    def __init__(self, db):
        self.db = db

    async def get_preference_by_id(self, user_id: int) -> Preference | None:
        stmt = select(Preference).where(Preference.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    

    async def create_preference(self, preference) -> PreferenceResponse:
        try:
            self.db.add(preference)
            await self.db.commit()  
            await self.db.refresh(preference)
            return PreferenceResponse.model_validate(preference)
                
        except Exception as e:
            await self.db.rollback()
            raise e
