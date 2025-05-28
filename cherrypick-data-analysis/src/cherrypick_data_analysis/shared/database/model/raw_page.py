from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from .category import Category
from .comment import Comment
from cherrypick_data_analysis.shared.enum.site import Site
from ..database import Base
from ...enum.price_type import PriceType
from sqlalchemy.dialects.mysql import MEDIUMTEXT


class RawPage(Base):
    __tablename__ = "raw_page"

    page_id = Column(BIGINT, primary_key=True, autoincrement=True)
    page_no = Column(BIGINT, nullable=True)
    raw_html = Column(MEDIUMTEXT , nullable=True)
    created_at = Column(DateTime, nullable=True)
    source_site = Column(Enum(Site), nullable=True)
