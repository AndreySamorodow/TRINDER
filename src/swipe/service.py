import json

from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.dependencies.swipe import create_access_token
from src.profile.schemas import ProfileResponseList
from src.kafka.service import KafkaService
from src.profile.preference.repository import PreferenceRepository
from src.profile.repository import ProfileRepository
from src.profile.models import Profile
from src.swipe.repository import SwipeRepository

from src.config import settings


class SwipeService:
    def __init__(self, db: AsyncSession, redis):
        self.db = db
        self.redis = redis
        self.swipe_repository = SwipeRepository(db)
        self.profile_repository = ProfileRepository(db)
        self.preference_repository = PreferenceRepository(db)
        self.kafka_service = KafkaService()


    async def get_profiles(
        self,
        response: Response,
        user_id: int,
        last_profile_id: Optional[int] = 0    # id последней анкеты из предыдущей выдачи
    ) -> List[Profile]:
        deck_key = f"deck:{user_id}"
        deck_json = await self.redis.get(deck_key)

        if deck_json:
            deck = json.loads(deck_json)

            if last_profile_id == 0:
                start_idx = 0
            else:
                try:
                    start_idx = deck.index(last_profile_id) + 1
                except ValueError:
                    start_idx = 0

            end_idx = start_idx + 30  # 30 профилей за раз
            next_ids = deck[start_idx:end_idx]

            if not next_ids:
                return ProfileResponseList(profiles=[])

            profiles = await self.profile_repository.get_profiles_by_ids(next_ids)
            profiles_dict = {p.id: p for p in profiles}
            # ВОТ ЗДЕСЬ — разворачиваем порядок
            sorted_profiles = [profiles_dict[pid] for pid in reversed(next_ids)]  # reversed()

            last_profile_id = next_ids[-1]  # последний в оригинальном порядке
            last_profile_id_token = create_access_token({"sub": str(last_profile_id)})
            response.set_cookie("TRINDER_LAST_PROFILE_ID", last_profile_id_token, httponly=True)

            return ProfileResponseList(profiles=sorted_profiles)

        else:
            current_profile = await self.profile_repository.get_profile_by_id(user_id)

            if not current_profile:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Profile not found")

            my_preferences = await self.preference_repository.get_preference_by_id(user_id)

            if not my_preferences:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")

            return await self.swipe_repository.get_profiles(
                response=response,
                user_id=user_id,
                profile=current_profile,
                preferences=my_preferences,
                last_profile_id=last_profile_id
                )


    async def swipe(self, user_id, swipe_id):
        swipe_user = await self.profile_repository.get_profile_by_id(swipe_id)
        user = await self.profile_repository.get_profile_by_id(user_id)

        if not swipe_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user does not exist")
        
        if user_id == swipe_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't swipe yourself")
        
        swipe = await self.swipe_repository.get_swipe(user1=user_id, user2=swipe_id)
        if swipe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You've already swiped this person")

        swipe = await self.swipe_repository.get_swipe(user1=swipe_id, user2=user_id)
        
        if swipe:  #если есть -> вставка и отправка брокеру сообщений, выдача доступа обоим к чату
            if swipe.decision2 == True:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You've already swiped this person")
            swipe.decision2 = True
            await self.db.commit()
            await self.kafka_service.notify_match(swipe_user.telegram_id, user.name)
        
        else:  #если нет -> создание в бд и отправка .вы понравились тому то.
            await self.swipe_repository.create_swipe(user1=user_id, user2=swipe_id)
            await self.kafka_service.notify_swipe(swipe_user.telegram_id, user.name)
