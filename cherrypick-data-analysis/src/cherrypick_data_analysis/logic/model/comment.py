from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from cherrypick_data_analysis.glob.enum.site import Site
from cherrypick_data_analysis.logic.model import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    content = Column(String(255), nullable=False)
    up_vote = Column(Integer, nullable=False)
    down_vote = Column(Integer, nullable=False)
    source_site = Column(Enum(Site), nullable=False)
    created_at = Column(DateTime, nullable=False)

    deal_id = Column(BIGINT, ForeignKey("deal.deal_id"), nullable=False)
    user_id = Column(BIGINT, ForeignKey("user.user_id"), nullable=False)

    # 관계 설정
    user = relationship("User", back_populates="comments")
    deal = relationship("Deal", back_populates="comments")