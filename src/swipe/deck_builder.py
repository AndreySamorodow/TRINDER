from sqlalchemy import select, and_, or_, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.profile.models import Profile
from src.profile.preference.models import Preference
from src.swipe.models import Swipe

class DeckBuilder:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def build_for_user(self, user_id: int) -> list[int]:
        profile_stmt = select(Profile).where(Profile.user_id == user_id)
        profile_result = await self.db.execute(profile_stmt)
        profile = profile_result.scalar_one_or_none()
        if not profile:
            return []

        pref_stmt = select(Preference).where(Preference.user_id == user_id)
        pref_result = await self.db.execute(pref_stmt)
        preferences = pref_result.scalar_one_or_none()
        if not preferences:
            return []

        stmt = (
            select(Profile.id)
            .outerjoin(Preference, Profile.user_id == Preference.user_id)
            .where(
                Profile.user_id != user_id,
                ~exists(
                    select(Swipe).where(
                        Swipe.user1 == user_id,
                        Swipe.user2 == Profile.user_id
                    )
                ),
                Profile.age.between(preferences.age - 2, preferences.age + 2),
                Profile.gender == preferences.gender,
                Profile.city == profile.city,
                or_(
                    Preference.id.is_(None),
                    and_(
                        Preference.age.between(profile.age - 2, profile.age + 2),
                        Preference.gender == profile.gender,
                    )
                )
            )
            .order_by(Profile.id.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
