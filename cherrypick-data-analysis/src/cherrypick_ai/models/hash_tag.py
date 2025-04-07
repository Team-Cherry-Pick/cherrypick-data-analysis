from sqlalchemy import Column, Integer, String, Text, DateTime, BIGINT
from sqlalchemy.orm import relationship

from src.cherrypick_ai.models import Base

class HashTag(Base):
    __tablename__ = "hash_tag"

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(255), nullable=False)
    # ✅ 다대다 관계 설정 (Tag ↔ Board)
    boards = relationship("Board", secondary="board_hashtag", back_populates="hash_tags")