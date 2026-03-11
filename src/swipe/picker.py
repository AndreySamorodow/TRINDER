from fastapi import HTTPException, status
from sqlalchemy import select, and_, not_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.profile.models import Profile
from src.profile.preference.models import Preference
from src.swipe.models import Swipe


class SwipeService:
    def __init__(self, db: AsyncSession):  # AsyncSession вместо Session
        self.db = db

    async def get_profiles(  # Добавили async
        self,
        current_user_id: int,
        limit: int = 20
    ) -> List[Profile]:
        # 1. Получаем текущий профиль пользователя
        stmt = select(Profile).where(Profile.user_id == current_user_id)
        result = await self.db.execute(stmt)
        current_profile = result.scalar_one_or_none()

        if not current_profile:
            return []

        # 2. Получаем предпочтения текущего пользователя
        stmt = select(Preference).where(Preference.user_id == current_user_id)
        result = await self.db.execute(stmt)
        my_preferences = result.scalar_one_or_none()

        if not my_preferences:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")

        # 3. Подзапрос: всех, кого я уже свайпнул
        swiped_users_subquery = (
            select(Swipe.user2)
            .where(Swipe.user1 == current_user_id)
            .subquery()
        )

        # 4. Подзапрос: всех, кто свайпнул меня
        swiped_me_subquery = (
            select(Swipe.user1)
            .where(Swipe.user2 == current_user_id)
            .subquery()
        )

        # 5. Основной запрос
        stmt = (
            select(Profile)
            .outerjoin(
                Preference, Profile.user_id == Preference.user_id
            )
            .where(
                # Не свой профиль
                Profile.user_id != current_user_id,

                # Не те, кого уже свайпнул
                not_(Profile.user_id.in_(swiped_users_subquery)),
                not_(Profile.user_id.in_(swiped_me_subquery)),

                # Условие 1: Анкета подходит МНЕ
                Profile.age >= my_preferences.age - 2,
                Profile.age <= my_preferences.age + 2,
                Profile.gender == my_preferences.gender,

                # Условие 2: Я подхожу анкете
                or_(
                    Preference.id.is_(None),  # если у анкеты нет предпочтений
                    and_(
                        Preference.age >= current_profile.age - 2,
                        Preference.age <= current_profile.age + 2,
                        Preference.gender == current_profile.gender,
                    )
                )
            )
            .order_by(Profile.id.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()