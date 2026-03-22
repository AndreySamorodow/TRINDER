from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)

    age = Column(Integer)
    gender = Column(String)

    user = relationship("User", back_populates="preference")

    __table_args__ = (
        Index('ix_preferences_user_gender_age', 'user_id', 'gender', 'age'),
    )
