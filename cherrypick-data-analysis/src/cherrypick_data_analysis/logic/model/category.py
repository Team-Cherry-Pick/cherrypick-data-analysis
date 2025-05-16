from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from cherrypick_data_analysis.glob.enum.site import Site
from cherrypick_data_analysis.logic.model import Base


class Category(Base):
    __tablename__ = "category"

    category_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    name = Column(String(255), nullable=False)

    deals = relationship("Deal", back_populates="category", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")