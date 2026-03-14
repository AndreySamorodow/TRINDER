from fastapi import HTTPException, Response, status
from sqlalchemy import select, and_, or_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.profile.schemas import ProfileResponseList
from src.dependencies.user import create_access_token
from src.profile.models import Profile
from src.profile.preference.models import Preference
from src.swipe.models import Swipe


class SwipeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profiles(
        self,
        response: Response,
        current_user_id: int,
        last_profile_id: Optional[int] = 0   # id последней анкеты из предыдущей выдачи
    ) -> List[Profile]:
        stmt = select(Profile).where(Profile.user_id == current_user_id)
        result = await self.db.execute(stmt)
        current_profile = result.scalar_one_or_none()

        if not current_profile:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Profile not found!")

        stmt = select(Preference).where(Preference.user_id == current_user_id)
        result = await self.db.execute(stmt)
        my_preferences = result.scalar_one_or_none()

        if not my_preferences:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")

        stmt = (
            select(Profile)
            .outerjoin(Preference, Profile.user_id == Preference.user_id)
            .where(
                Profile.user_id != current_user_id,
                ~exists(
                    select(Swipe).where(
                        Swipe.user1 == current_user_id,
                        Swipe.user2 == Profile.user_id
                    )
                ),
                Profile.age.between(my_preferences.age - 2, my_preferences.age + 2),
                Profile.gender == my_preferences.gender,
                Profile.city == current_profile.city,
                or_(
                    Preference.id.is_(None),
                    and_(
                        Preference.age.between(current_profile.age - 2, current_profile.age + 2),
                        Preference.gender == current_profile.gender,
                    )
                )
            )
        )

        if last_profile_id != 0:
            stmt = stmt.where(Profile.id > last_profile_id)

        stmt = stmt.order_by(Profile.id.desc()).limit(30)

        result = await self.db.execute(stmt)
        profiles = result.scalars().all()

        if profiles:
            last_profile_id = profiles[-1].id
        else:
            last_profile_id = last_profile_id

        last_profile_id_token = create_access_token({"sub": str(last_profile_id)})
        response.set_cookie("TRINDER_LAST_PROFILE_ID", last_profile_id_token, httponly=True)

        return ProfileResponseList(profiles=list(reversed(profiles)))
