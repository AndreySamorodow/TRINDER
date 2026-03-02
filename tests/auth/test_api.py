from httpx import AsyncClient

async def test_register(ac: AsyncClient):
    res = await ac.post(
        url="api/auth/register",
        json={
            "email": "test.api@test.com",
            "password": "testpassword",
            "password_replay": "testpassword",
        }
    )
    assert res.status_code == 200


async def test_login(ac: AsyncClient):
    res = await ac.post(
        url="api/auth/login",
        json={
            "email": "test.api@test.com",
            "password": "testpassword"
        }
    )
    assert res.status_code == 200


async def test_get_google_oauth_redirect_uri(
    ac: AsyncClient, 
    mock_google_oauth_service_exact,
    mock_redis
):
    response = await ac.get("/api/oauth/google/url", follow_redirects=False)
    assert response.status_code == 302
    
