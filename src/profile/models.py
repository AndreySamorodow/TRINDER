from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    photo = Column(String, default="https://9e72a0d7-ed69-469e-9eed-34406680ef1c.selstorage.ru/0")
    telegram_id = Column(Integer)

    user = relationship("User", back_populates="profile")

    __table_args__ = (
        Index('ix_profiles_search', 'gender', 'city', 'age', 'user_id'),
    )
