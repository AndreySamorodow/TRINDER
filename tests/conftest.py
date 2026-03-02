from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
import pytest
from unittest.mock import AsyncMock, patch

from src.database.database import Base, get_session
from src.main import app

engine = create_async_engine(
    url="sqlite+aiosqlite:///./test.db"
)

async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function")
async def session():
    async with new_session() as session:
        yield session

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_google_oauth_service_exact():
    """
    Мок для OAuthService - ПРОВЕРЕННЫЙ РАБОЧИЙ ВАРИАНТ
    """
    # Патчим прямо в том месте, где класс импортируется в роутер
    with patch('src.auth.oauth.router.OAuthService') as MockService:
        
        # Создаем мок экземпляра
        mock_instance = AsyncMock()
        mock_instance.generate_google_oauth_redirect_uri = AsyncMock()
        
        # Устанавливаем возвращаемое значение
        test_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            "state=test_state_12345&"
            "client_id=test_client_id&"
            "redirect_uri=http://localhost:5500/auth/google&"
            "response_type=code&"
            "scope=openid%20profile%20email&"
            "access_type=offline"
        )
        
        mock_instance.generate_google_oauth_redirect_uri.return_value = test_url
        
        # ВАЖНО: при вызове OAuthService(redis) возвращаем наш мок
        MockService.return_value = mock_instance
        
        yield mock_instance

@pytest.fixture
def mock_redis():
    """
    Мок для Redis - ПРОВЕРЕННЫЙ РАБОЧИЙ ВАРИАНТ
    """
    # Создаем мок Redis клиента
    mock_redis_client = AsyncMock()
    mock_redis_client.setex = AsyncMock(return_value=True)
    mock_redis_client.get = AsyncMock(return_value="pending")
    mock_redis_client.ping = AsyncMock(return_value=True)
    
    # Создаем мок для redis_manager
    mock_redis_manager = AsyncMock()
    mock_redis_manager.is_connected = True
    mock_redis_manager.client = mock_redis_client
    
    # Патчим всё необходимое
    with patch('src.core.redis.get_redis', return_value=mock_redis_client):
        with patch('src.core.redis.redis_manager', mock_redis_manager):
            yield mock_redis_client