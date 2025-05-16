from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from cherrypick_data_analysis.glob.enum.site import Site
from cherrypick_data_analysis.logic.model import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    nickname = Column(String(255), nullable=False)
    source_site = Column(Enum(Site), nullable=False)
    first_appear_date = Column(DateTime, nullable=False)

    deals = relationship("Deal", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")