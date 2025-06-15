from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from cherrypick_data_analysis.shared.enum.site import Site
from ..database import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    content = Column(String(255), nullable=False)
    up_vote = Column(Integer, nullable=False)
    down_vote = Column(Integer, nullable=False)
    source_site = Column(Enum(Site), nullable=False)
    created_at = Column(DateTime, nullable=False)
    username = Column(String(100), nullable=False)
    deal_id = Column(BIGINT, ForeignKey("deal.deal_id"), nullable=False)


    # 관계 설정
    deal = relationship("Deal", back_populates="comments", cascade="all")