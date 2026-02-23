from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    user = relationship("User", back_populates="profile")
    preferences = relationship("Preference", back_populates="profile", uselist=False, cascade="all, delete-orphan")



class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    age = Column(Integer)
    gender = Column(String)

    profile = relationship("Profile", back_populates="preferences")