from fastapi import HTTPException, status

from src.profile.preference.models import Preference
from src.profile.preference.schemas import PreferenceCreate, PreferenceResponse
from src.profile.preference.repository import PreferenceRepository


class PreferenceService:
    def __init__(self, db):
        self.db = db
        self.preference_repository = PreferenceRepository(db)

    async def get_preference(self, user_id: int):
        preference = await self.preference_repository.get_preference_by_id(user_id)
        if not preference:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferense not found")
        return PreferenceResponse.model_validate(preference)
    
    async def create_or_change_preference(self, user_id: int, user_data: PreferenceCreate):
        existing_preference = await self.preference_repository.get_preference_by_id(user_id)

        preference_dict = user_data.model_dump()
        preference_dict["user_id"] = user_id
        preference_dict["id"] = user_id
        


        if existing_preference:
            for key, value in preference_dict.items():
                setattr(existing_preference, key, value)
            
            await self.db.commit()
            await self.db.refresh(existing_preference)
            return existing_preference
        else:
            new_profile = Preference(**preference_dict)
            return await self.preference_repository.create_preference(new_profile)
        
