from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
import jwt

from src.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


def get_token(request: Request):
    token = request.cookies.get("TRINDER_LAST_PROFILE_ID")
    return token

async def get_last_profile_id(token = Depends(get_token)):
    if token:
        try:
            payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        expire = payload.get("exp")
        if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
            return 0
        last_profile_id = payload.get("sub")
        if not last_profile_id:
            return 0
                
        return int(last_profile_id)
    
    else:
        return 0

LastProfileId = Annotated[int, Depends(get_last_profile_id)]
