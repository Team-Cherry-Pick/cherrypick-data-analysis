from datetime import datetime

from bs4 import BeautifulSoup, Tag

from shared.enum.site import Site
from shared.database.query.raw_query import get_created_at
from shared.process.page_dto import CommentDTO

site = Site.PPOMPPU

def parse_comment(no, soup: BeautifulSoup):
    comment_lines = soup.find_all("div", class_="comment_line")
    comments = []
    for comment in comment_lines:
        comments.append(
            CommentDTO(
                deal_no=no,
                source_site=site,
                username=parse_username(comment),
                content=parse_content(comment),
                upvote=parse_upvote(comment),
                downvote=parse_downvote(comment),
                created_at=parse_datetime(comment, no)
            )
        )

    return comments

def parse_username(comment_div: Tag) -> str:
    """
    댓글 블록에서 작성자 닉네임 추출.

    우선순위:
    1. <img alt="닉네임">이 있으면 alt 속성 사용
    2. <b> 태그 내 텍스트가 있으면 해당 텍스트 사용
    3. 아무것도 없으면 '익명' 반환
    """
    b_tag = comment_div.find("b")
    if not b_tag:
        return "[* 비회원 *]"

    # 1. 이미지 닉네임 우선
    img_tag = b_tag.find("img")
    if img_tag and img_tag.has_attr("alt") and img_tag["alt"].strip():
        return img_tag["alt"].strip()

    # 2. 텍스트 닉네임
    nickname = b_tag.get_text(strip=True)
    if nickname:
        return nickname

    # 3. fallback
    return "[* 비회원 *]"


def parse_content(comment_div: Tag) -> str:
    """
    댓글 블록에서 내용 텍스트를 추출한다.

    <div id="commentContent_XXXX"> 내부의 텍스트를 정리해 반환.
    줄바꿈은 <br> 기준.
    """
    content_div = comment_div.find("div", class_="mid-text-area")
    if not content_div:
        return ""

    # <br> → \n 변환
    for br in content_div.find_all("br"):
        br.replace_with("\n")

    # 전체 텍스트 정리
    return content_div.get_text(separator="", strip=True)

from bs4.element import Tag

def parse_upvote(comment_div: Tag) -> int:
    """
    댓글 블록에서 추천 수(upvote)를 정수로 추출한다.

    <span id="vote_cnt_XXXX"> 에 있는 숫자 사용.
    """
    vote_span = comment_div.find("span", id=lambda x: x and x.startswith("vote_cnt_"))
    if vote_span and vote_span.text.strip().isdigit():
        return int(vote_span.text.strip())
    return 0

def parse_downvote(comment_div: Tag) -> int:
    downvote_span = comment_div.find("span", id=lambda x: x and x.startswith("anti_vote_cnt_"))
    if downvote_span and downvote_span.text.strip().isdigit():
        return int(downvote_span.text.strip())
    return 0


def parse_datetime(comment_div: Tag, no: int) -> datetime:
    """
    댓글 블록에서 작성일시를 추출하여 datetime 객체로 반환.
    - HH:MM:SS 형식이면 오늘 날짜 + 시간 결합
    - YYYY-MM-DD HH:MM:SS 형식이면 그대로 사용
    """
    time_tag = comment_div.find("font", class_="eng-day")
    if not time_tag:
        return datetime.now()  # fallback
    raw = time_tag.get("title") or time_tag.text.strip()
    raw = raw.replace(" *", "")

    try:
        if len(raw) == 8 and raw.count(":") == 2:  # HH:MM:SS
            time_part = datetime.strptime(raw, "%H:%M:%S").time()
            today_date = get_created_at(no, site).date()
            return datetime.combine(today_date, time_part)
        else:  # YYYY-MM-DD HH:MM:SS
            return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"[ERROR] parse_datetime: {e} {raw}")
        return datetime.now()