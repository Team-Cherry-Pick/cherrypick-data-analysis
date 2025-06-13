import bs4
import re
import datetime
from shared.save_process.page_dto import DealDTO
from shared.enum.price_type import PriceType
from shared.enum.site import Site
from shared.util.global_parse_util import get_store
from shared.util.redis_util import save_error_log

site = Site.PPOMPPU
def parse_deal(no, soup: bs4.BeautifulSoup) :

    link = get_link(no, soup)
    title = get_title(no, soup)
    is_blinded = True if "해당글은 운영자에 의해 블라인드 처리된 글입니다." in soup.text else False
    if is_blinded : print(no)
    return DealDTO(
        source_site=site,
        deal_no=no,
        username=get_username(no, soup),
        title=title,
        content=get_content(no, soup),

        price_type=get_currency_from_title(no, soup),
        origin_price=title,
        discounted_price=get_price_from_title(no, soup),
        vote=get_vote(no, soup),
        views=get_views(no, soup),
        comment_count=get_comment_count(no, soup),
        is_expired=get_is_expired(no, soup),
        is_blinded = is_blinded,

        store=get_store(link),
        product_link=link,
        created_at=get_datetime(no, soup)
    )



def get_username(no, soup: bs4.BeautifulSoup) :
    try :
        user_tag = soup.select_one("strong a.baseList-name")
        if user_tag:
            # 1. 텍스트가 존재하면 우선 사용
            username = user_tag.text.strip()
            if username:
                return username

            # 2. 텍스트 없으면 <img alt="닉네임"> 추출
            img_tag = user_tag.select_one("img[alt]")
            if img_tag and "alt" in img_tag.attrs:
                return img_tag["alt"].strip()

        return None

    except AttributeError as e :
        save_error_log(site, "username parsing error", {"no": no, "error": str(e)})
        return None


def get_title(no, soup: bs4.BeautifulSoup) :
    try :
        # 제목 메타 태그에서 content 추출
        title_tag = soup.select_one('meta[property="og:title"]')
        title = title_tag["content"].strip() if title_tag and "content" in title_tag.attrs else None

        return title
    except AttributeError as e :
        save_error_log(site, "title parsing error", {"no" : no, "error" : str(e)})
        return None

def get_content(no, soup: bs4.BeautifulSoup) :
    try :
        # 본문 요약 메타 태그에서 content 추출
        content_tag = soup.select_one('meta[property="og:description"]')
        content = content_tag["content"].strip() if content_tag and "content" in content_tag.attrs else None

        return content
    except AttributeError as e :
        save_error_log(site, "content parsing error", {"no" : no, "error" : str(e)})
        return None


def get_is_expired(no, soup: bs4.BeautifulSoup) :
    try :
        expired_tag = soup.select_one("div.top_cmt")
        is_expired = (
            expired_tag is not None and
            "품절 / 종결 / 취소된 게시물입니다." in expired_tag.text
        )

        return is_expired
    except AttributeError as e :
        save_error_log(site, "is_expired parsing error", {"no" : no, "error" : str(e)})
        return None


def get_vote(no, soup: bs4.BeautifulSoup) :
    try :
        # 추천수 추출
        up_tag = soup.select_one("#vote_list_btn_txt")
        upvote = int(up_tag.text.strip()) if up_tag else 0

        # 비추천수 추출
        down_tag = soup.select_one("#vote_anti_list_btn_txt")
        downvote = int(down_tag.text.strip()) if down_tag else 0

        return upvote - downvote
    except AttributeError as e :
        save_error_log(site, "vote parsing error", {"no" : no, "error" : str(e)})
        return None



def get_comment_count(no, soup: bs4.BeautifulSoup) :
    try:
        comment_count = len([tag for tag in soup.find('font', class_='pagelist_han').children if getattr(tag, 'name', None)])
        return comment_count
    except Exception as e:
        save_error_log(Site.PPOMPPU, "COMMENT PARSING ERROR", {"message" : e, "is_blinded" : True if "해당글은 운영자에 의해 블라인드 처리된 글입니다." in soup.text else False, "no" : no})
        return 0

def get_link(no, soup: bs4.BeautifulSoup) :
    try :
        link_tag = soup.select_one("li.topTitle-link > a")
        link = link_tag.text.strip() if link_tag else None

        return link
    except AttributeError as e :
        save_error_log(site, "link parsing error", {"no" : no, "error" : str(e)})
        return None

def get_datetime(no, soup: bs4.BeautifulSoup) -> datetime:
    try :
        date_li = soup.select_one("ul.topTitle-mainbox > li:nth-of-type(2)")
        if date_li and "등록일" in date_li.text:
            raw = date_li.text.replace("등록일", "").strip()  # "2025-06-10 11:11"
            dt = datetime.datetime.strptime(raw, "%Y-%m-%d %H:%M")
            return dt  # 정확히 원하는 포맷
        else:
            return None
    except Exception as e :
        save_error_log(site, "datetime parsing error", {"no" : no, "error" : str(e)})
        return None

def get_views(no, soup: bs4.BeautifulSoup) :
    try :
        view_li = soup.select_one("ul.topTitle-mainbox > li:nth-of-type(3)")
        if view_li and "조회수" in view_li.text:
            view_text = view_li.text.replace("조회수", "").strip().replace(",", "")
            views = int(view_text)
        else:
            views = None

        return views
    except (AttributeError, ValueError) as e :
        save_error_log(site, "views parsing error", {"no" : no, "error" : str(e)})
        return None


def get_price_from_title(no, soup: bs4.BeautifulSoup):
    try:
        title_tag = soup.select_one('meta[property="og:title"]')
        title = title_tag["content"] if title_tag and "content" in title_tag.attrs else ""

        # 괄호 안 추출
        bracket_matches = re.findall(r"\(([^)]+)\)", title)
        for text in bracket_matches:
            # 쉼표 제거
            text = text.replace(",", "").lower()

            # USD 처리
            usd_match = re.search(r"(?:usd|\$)\s?(\d+(?:\.\d+)?)", text)
            if usd_match:
                return int(float(usd_match.group(1)))

            # 일반 숫자 처리: 문자 제거 후 숫자만 추출
            numbers = re.findall(r"\d+", text)
            if numbers:
                return int(numbers[0])  # 첫 번째 숫자만 사용

        return None

    except Exception as e:
        save_error_log(site, "price parsing error", {"no": no, "error": str(e)})
        return None


def get_currency_from_title(no, soup: bs4.BeautifulSoup) :
    try :
        title_tag = soup.select_one('meta[property="og:title"]')
        title = title_tag["content"] if title_tag and "content" in title_tag.attrs else ""

        # 괄호 안만 대상으로 함
        bracket_contents = re.findall(r"\(([^)]+)\)", title)

        for content in bracket_contents:
            # 1. USD 여부
            if re.search(r"(usd|\$)", content, re.IGNORECASE):
                return PriceType.USD

            # 2. 정수 숫자가 있으면 krw로 판단
            if re.search(r"\b[\d,]+\b", content):
                return PriceType.KRW

        return PriceType.KRW  # 가격 정보 없음

    except Exception as e :
        save_error_log(site, "currency parsing error", {"no": no, "error": str(e)})
        return PriceType.KRW
