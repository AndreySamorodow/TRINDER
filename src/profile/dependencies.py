import json

from fastapi import Form, HTTPException
from src.profile.schemas import ProfileCreate


async def parse_profile_create(profile_data: str = Form(..., alias="user_data")) -> ProfileCreate:
    try:
        user_dict = json.loads(profile_data)
        return ProfileCreate(**user_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")