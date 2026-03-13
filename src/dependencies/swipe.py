from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
import jwt

from src.config import settings

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
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
                
        return int(user_id)
    
    else:
        return None

UserId = Annotated[int, Depends(get_last_profile_id)]
