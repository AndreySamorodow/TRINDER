from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError

from src.config import settings    

import jwt

def get_token(request: Request):
    token = request.cookies.get("TRINDER_ACCESS_TOKEN")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

async def get_user_id(token = Depends(get_token)):
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

UserId = Annotated[int, Depends(get_user_id)]