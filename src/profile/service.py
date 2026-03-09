from fastapi import HTTPException, status

from src.profile.models import Profile
from src.profile.schemas import ProfileCreate, ProfileResponse
from src.profile.repository import ProfileRepository
from src.profile.S3.service import S3Service


class ProfileService:
    def __init__(self, db):
        self.db = db
        self.profile_repository = ProfileRepository(db)
        self.s3_service = S3Service()

    async def get_profile(self, user_id) -> ProfileResponse:
        profile = await self.profile_repository.get_profile_by_id(user_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profil not found")
        return ProfileResponse.model_validate(profile)

    async def create_or_change_profile(self, user_id: int, user_data: ProfileCreate, photo) -> ProfileResponse:
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
            return existing_profile
        else:
            new_profile = Profile(**profile_dict)
            return await self.profile_repository.create_profile(new_profile)
