from sqlalchemy import insert, select, update
from src.auth.models import User


class BaseDao:
    model = None

    @classmethod
    async def find_one_or_none(cls, db, **filters):
        query = select(cls.model).filter_by(**filters)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, db, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, db, **data):
        query = insert(cls.model).values(**data)
        await db.execute(query)
        await db.commit()

    @classmethod
    async def change(cls, db, id, **data):
        try:
            query = update(cls.model).where(cls.model.id == id).values(**data)
            await db.execute(query)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e

class UserDao(BaseDao):
    model = User
