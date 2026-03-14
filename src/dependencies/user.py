import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.config import settings    

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=1024,
    argon2__time_cost=2,
    argon2__parallelism=1
)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


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