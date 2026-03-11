from sqlalchemy import Boolean, Column, Integer
from src.database.database import Base

class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True)
    user1 = Column(Integer, nullable=False)
    user2 = Column(Integer, nullable=False)
    decision1 = Column(Boolean, nullable=False, default=True)
    decision2 = Column(Boolean)
