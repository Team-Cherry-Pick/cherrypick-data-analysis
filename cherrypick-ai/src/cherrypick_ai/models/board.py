from sqlalchemy import Column, Integer, String, Text, DateTime, BIGINT, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.testing.schema import Table
from src.cherrypick_ai.models import Base

# ✅ 중간 테이블 (다대다 관계를 위한 Association Table)
board_hashtag = Table(
    "board_hashtag",
    Base.metadata,
    Column("board_id", Integer, ForeignKey("board.board_id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("hash_tag.tag_id"), primary_key=True),
)

class Board(Base):
    __tablename__ = "board"

    board_id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    content = Column(String(255), nullable=False)  # ✅ VARCHAR(255), NOT NULL
    price = Column(Integer, nullable=True)  # ✅ INT, NULL 가능
    title = Column(String(255), nullable=False)  # ✅ VARCHAR(255), NOT NULL
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)  # ✅ 외래 키 (user_id)


    user = relationship("User", back_populates="boards")
    hash_tags = relationship("HashTag", secondary="board_hashtag", back_populates="boards")
