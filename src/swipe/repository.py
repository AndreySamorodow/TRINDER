from fastapi import Response
from sqlalchemy import select, and_, or_, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.swipe import create_access_token
from src.profile.models import Profile
from src.profile.preference.models import Preference
from src.profile.schemas import ProfileResponseList
from src.swipe.models import Swipe


class SwipeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profiles(
            self,
            response: Response,
            user_id: int,
            profile: Profile,
            preferences: Preference,
            last_profile_id: int
        ) -> ProfileResponseList:
        stmt = (
            select(Profile)
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


    async def get_swipe(self, **filters):
        stmt = select(Swipe).filter_by(**filters)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def create_swipe(self, user1, user2):
        swipe_dict = {
            "user1":user1,
            "user2":user2,
            "decision1":True,
        }
        
        swipe = Swipe(**swipe_dict)
        try:
            self.db.add(swipe)
            await self.db.commit()  
            await self.db.refresh(swipe)
                
        except Exception as e:
            await self.db.rollback()
            raise e
