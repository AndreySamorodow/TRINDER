import json
import logging

from sqlalchemy import select

from src.auth.models import User
from src.profile.models import Profile
from src.core.redis import redis_manager
from src.database.database import new_session
from src.swipe.deck_builder import DeckBuilder

logger = logging.getLogger(__name__)


async def build_decks_job(current_user_id: int = None):
    await redis_manager.start()
    redis = redis_manager.client
        
    async with new_session() as db:
        if not current_user_id:
            stmt = select(User.id).join(Profile).where(Profile.id.isnot(None))
            result = await db.execute(stmt)
            user_ids = result.scalars().all()
            
        else: 
            user_ids = [current_user_id]

        builder = DeckBuilder(db)
            
        for user_id in user_ids:
            try:
                deck = await builder.build_for_user(user_id)
                key = f"deck:{user_id}"
                    
                if deck:
                    await redis.setex(key, 86400, json.dumps(deck))
                else:
                    await redis.delete(key)
                        
            except Exception as e:
                logger.error(f"Error for user {user_id}: {e}")
