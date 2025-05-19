from dataclasses import dataclass
from datetime import datetime
from typing import List

from shared.enum.site import Site

@dataclass
class CommentDTO:
    deal_no: int
    content: str
    username: str
    upvote: int
    downvote: int
    source_site: Site
    created_at: datetime

@dataclass
class DealDTO :
    source_site: Site
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


@dataclass
class UserDTO:
    username: str
    appear_time: datetime
    source_site: Site
    behavior: str

@dataclass
class PageDTO:
    deal: DealDTO
    comments: List[CommentDTO]
    users: List[UserDTO]
    next_page: int
