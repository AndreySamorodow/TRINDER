from typing import Annotated

from fastapi import APIRouter, Body, Response
from fastapi.responses import RedirectResponse

import jwt

from src.database.database import DbSession
from src.auth.oauth.service import OAuthService
from src.core.redis import RedisSession


router = APIRouter(prefix="/api/oauth", tags=["Auth"])

@router.get("/google/url")
async def get_google_oauth_redirect_uri(redis: RedisSession):
    service = OAuthService(redis)
    uri = await service.generate_google_oauth_redirect_uri()
    return RedirectResponse(url=uri, status_code=302)

@router.post("/google/callback")
async def handle_code(
    response: Response,
    db: DbSession,
    code: Annotated[str, Body()],
    state: Annotated[str, Body()],
    redis: RedisSession
):
    service = OAuthService(redis)
    await service.verify_state(state)

    token_data = await service.exchange_google_code(code)
    id_token = token_data["id_token"]
    user_data = service.decode_google_token(id_token)

    return await service.login_with_oauth(response, db, user_data["email"])
