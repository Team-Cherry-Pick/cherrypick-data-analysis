from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from cherrypick_data_analysis.glob.enum.site import Site
from cherrypick_data_analysis.logic.model import Base


class Deal(Base):
    __tablename__ = "deal"

    deal_id = Column(BIGINT, primary_key=True, autoincrement=True)  # ✅ 기본 키, 자동 증가
    deal_no = Column(BIGINT, nullable=False)  # ✅ 해당 사이트에서 번호
    title = Column(String(255), nullable=False)  # ✅ VARCHAR(255), NOT NULL
    content = Column(String(255), nullable=False)  # ✅ VARCHAR(255), NOT NULL
    product_link = Column(String(255), nullable=False)
    store = Column(String(255), nullable=False)             # 어떤 스토어인지 (쿠팡, 지마켓 등 / 해당 사이트의 title 값을 받아옴)
    vote = Column(Integer, nullable=False)                  # 추천 - 비추천
    created_at = Column(DateTime, nullable=False)           # 생성일

    origin_price = Column(Integer, nullable=True)           # 원래 가격
    discounted_price = Column(Integer, nullable=True)       # 할인된 가격

    is_published = Column(Boolean, nullable=False)          # 실 서비스에 발행되었나?
    source_site = Column(Enum(Site), nullable=False)        # 데이터를 받아온 사이트

    user_id = Column(BIGINT, ForeignKey("user.user_id"), nullable=False)  # 외래 키 (user_id)
    category_id = Column(BIGINT, nullable=True)          # 카테고리

    user = relationship("User", back_populates="deals")
    category = relationship("Category", back_populates="deals")
    comments = relationship("Comment", back_populates="deal", cascade="all, delete-orphan")
