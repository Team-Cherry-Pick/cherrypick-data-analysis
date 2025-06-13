from dataclasses import dataclass
from datetime import datetime
from typing import List

from shared.database.model import Category
from shared.enum.price_type import PriceType
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

    price_type: PriceType
    origin_price: str
    discounted_price: int
    vote: int
    views: int
    comment_count: int
    is_expired : bool
    is_blinded: bool

    store: str
    product_link: str
    created_at: datetime
    category_id: int | None


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


def get_users(source_site:Site, deal:DealDTO, comments:List[CommentDTO]) -> List[UserDTO]:
    users = [UserDTO(deal.username, deal.created_at, source_site=source_site, behavior="DEAL")]
    for comment in comments:
        user = next((u for u in users if u.username == comment.username), None)
        if user is None:
            users.append(UserDTO(comment.username, comment.created_at, source_site=source_site, behavior="COMMENT"))
    return users