from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from src.cherrypick_ai.database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    username = Column(String(255), unique=True, nullable=False)  # ✅ VARCHAR(255), 고유값 (unique)
    password = Column(String(255), nullable=False)  # ✅ VARCHAR(255), NOT NULL

    # ✅ Board 테이블과 관계 설정 (한 사용자가 여러 게시글 작성 가능)
    boards = relationship("Board", back_populates="user")
