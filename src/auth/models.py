from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String)
    password = Column(String)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
