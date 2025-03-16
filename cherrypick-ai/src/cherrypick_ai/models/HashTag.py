from sqlalchemy import Column, Integer, String, Text, DateTime, BIGINT
from src.cherrypick_ai.models import Base

class HashTag(Base):
    __tablename__ = "hash_tag"

    tagId = Column(BIGINT, primary_key=True)
    tagName = Column(String(255), nullable=False)