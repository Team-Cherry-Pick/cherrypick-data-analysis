from sqlalchemy import Column, String, BIGINT
from sqlalchemy.orm import relationship

from ..database import Base


class Category(Base):
    __tablename__ = "category"

    category_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    name = Column(String(255), nullable=False)

    deals = relationship("Deal", back_populates="category", cascade="all, delete-orphan")