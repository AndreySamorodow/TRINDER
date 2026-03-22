import uuid

from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.profile.models import Profile
from src.profile.schemas import ProfileCreate, ProfileResponse
from src.profile.repository import ProfileRepository
from src.profile.S3.service import S3Service


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.profile_repository = ProfileRepository(db)
        self.s3_service = S3Service()

    async def get_profile(self, user_id) -> ProfileResponse:
        profile = await self.profile_repository.get_profile_by_id(user_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profil not found")
        return ProfileResponse.model_validate(profile)

    async def create_or_change_profile(self, redis, user_id: int, user_data: ProfileCreate, photo) -> ProfileResponse:
        existing_profile = await self.profile_repository.get_profile_by_id(user_id=user_id)

        profile_dict = user_data.model_dump()
        profile_dict["user_id"] = user_id
        profile_dict["id"] = user_id

        if photo:
            if not photo.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")

            contents = await photo.read()
            url_photo = await self.s3_service.add_photo_to_s3(photo=contents, name=str(user_id))
            profile_dict["photo"] = url_photo


        if existing_profile:
            for key, value in profile_dict.items():
                setattr(existing_profile, key, value)

            await self.db.commit()
            await self.db.refresh(existing_profile)

            await self.profile_repository.rebuild_user_deck(user_id, redis)

            return existing_profile
        else:
            new_profile = Profile(**profile_dict)
            profile = await self.profile_repository.create_profile(new_profile)
            await self.profile_repository.rebuild_user_deck(user_id, redis)
            return profile


    async def get_link_tg_url(self, user_id: int, redis):
        secret_code = str(uuid.uuid4())
        await redis.setex(f"tg_auth:{secret_code}", 120, user_id)
        return f"https://t.me/trinder_bot?start={secret_code}"

    async def bind_tg_account(self, data, redis):
        user_id = await redis.get(f"tg_auth:{data.code}")  # Возвращает "42"!
    
        if not user_id:
            raise HTTPException(status_code=404)
        
        stmt = (
            update(Profile)
            .where(Profile.id == int(user_id))
            .values(
                telegram_id=data.telegram_id
            )
        )
        
        result = await self.db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        await self.db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK)
    