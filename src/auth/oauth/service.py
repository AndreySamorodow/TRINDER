import aiohttp
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
import jwt

from src.auth.dependencies import create_access_token
from src.database.dao import UserDao
from src.config import settings

import urllib.parse
import secrets


class OAuthService:
    def __init__(self, redis):
        self.redis = redis

    async def generate_google_oauth_redirect_uri(self):
        state = secrets.token_urlsafe(16)
        await self.redis.setex(name=f"state_oauth_google:{state}", time=60, value="pending")
        
        query_params = {
            "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
            "redirect_uri": "http://localhost:5500/auth/google",
            "response_type": "code",
            "scope": " ".join([
                "openid",
                "profile",
                "email"
            ]),
            "access_type": "offline",
            "state": state
        }

        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

        return f"{base_url}?{query_string}"
    

    async def verify_state(self, state):
        if await self.redis.get(f"state_oauth_google:{state}") != "pending":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        await self.redis.delete(f"state_oauth_google:{state}")


    async def exchange_google_code(self, code):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://oauth2.googleapis.com/token",
                data = {
                    "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
                    "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": "http://localhost:5500/auth/google",
                    "code": code,
                },
                ssl = False
            ) as response:
                
                return await response.json()
            
    def decode_google_token(self, id_token):
        return jwt.decode(
                id_token,
                algorithms=["RS256"],
                options={"verify_signature": False}
            )
        

    async def login_with_oauth(self, response, db, email):
        user = await UserDao.find_one_or_none(db, email=email)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            response.set_cookie("TRINDER_ACCESS_TOKEN", access_token, httponly=True)
        else:
            await UserDao.add(db=db, email=email, oauth=True)

        return RedirectResponse(url="http://localhost:5500", status_code=200)
