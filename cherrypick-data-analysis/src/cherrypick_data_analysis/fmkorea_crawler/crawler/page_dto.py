from dataclasses import dataclass
from datetime import datetime
from typing import List

from cherrypick_data_analysis.shared.enum import Site

@dataclass
class CommentDTO:
    content: str
    username: str
    upvote: int
    downvote: int
    created_at: datetime

@dataclass
class DealDTO :
    source_site: Site
    next_page: int
    deal_no: int
    username: str
    title: str
    content: str

    origin_price: int
    discounted_price: int
    vote: int
    views: int
    comment_count: int
    is_expired : bool

    store: str
    product_link: str
    created_at: datetime

    comment_list: List[CommentDTO]
