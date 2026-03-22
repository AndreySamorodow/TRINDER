from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, UniqueConstraint
from src.database.database import Base

class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True)
    user1 = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    user2 = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    decision1 = Column(Boolean, nullable=False, default=True)
    decision2 = Column(Boolean)

    __table_args__ = (
        Index('ix_swipes_user1_user2', 'user1', 'user2', unique=True),
        Index('ix_swipes_user2_user1', 'user2', 'user1'),
        UniqueConstraint('user1', 'user2', name='uq_swipes_user1_user2'),
    )
