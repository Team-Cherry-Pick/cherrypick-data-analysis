from sqlalchemy import Column, String, BIGINT, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from cherrypick_data_analysis.shared.enum.site import Site
from ..database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    username = Column(String(255), nullable=False)
    source_site = Column(Enum(Site), nullable=False)
    first_appear_time = Column(DateTime, nullable=False)
    last_appear_time = Column(DateTime, nullable=False)

    deals = relationship("Deal", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('username', 'source_site', name='uq_username_source_site'),
    )