from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from .category import Category
from .comment import Comment
from cherrypick_data_analysis.shared.enum.site import Site
from ..database import Base

class Deal(Base):
    __tablename__ = "deal"

    deal_id = Column(BIGINT, primary_key=True, autoincrement=True)
    deal_no = Column(BIGINT, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    product_link = Column(String(255), nullable=False)
    views = Column(Integer, nullable=False)
    store = Column(String(255), nullable=True)
    vote = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    is_expired = Column(Boolean, nullable=False)
    origin_price = Column(Integer, nullable=True)
    discounted_price = Column(Integer, nullable=True)
    source_site = Column(Enum(Site), nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    user_id = Column(BIGINT, ForeignKey("user.user_id"), nullable=False)
    category_id = Column(BIGINT, ForeignKey("category.category_id"), nullable=True)

    user = relationship("User", back_populates="deals")
    category = relationship("Category", back_populates="deals")
    comments = relationship("Comment", back_populates="deal", cascade="all, delete-orphan")
