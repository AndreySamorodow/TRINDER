from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


from src.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)
    oauth = Column(Boolean, nullable=False, default=False)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
