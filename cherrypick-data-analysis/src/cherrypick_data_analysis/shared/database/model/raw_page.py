from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from .category import Category
from .comment import Comment
from cherrypick_data_analysis.shared.enum.site import Site
from ..database import Base
from ...enum.price_type import PriceType


class Deal(Base):
    __tablename__ = "deal"

    deal_id = Column(BIGINT, primary_key=True, autoincrement=True)
    deal_no = Column(BIGINT, nullable=True)


    source_site = Column(Enum(Site), nullable=True)
    is_published = Column(Boolean, nullable=True, default=False)
    user_id = Column(BIGINT, ForeignKey("user.user_id"), nullable=True)
    category_id = Column(BIGINT, ForeignKey("category.category_id"), nullable=True)

    user = relationship("User", back_populates="deals")
    category = relationship("Category", back_populates="deals")
    comments = relationship("Comment", back_populates="deal", cascade="all, delete-orphan")
