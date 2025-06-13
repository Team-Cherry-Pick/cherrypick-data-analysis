import math

from bs4 import BeautifulSoup
from shared.util.crawl_util import parse_html
from shared.process.page_dto import CommentDTO
from shared.enum.site import Site
from shared.util.global_parse_util import parse_date_time
from shared.util.redis_util import save_error_log

# 해당 글의 댓글을 전부 가져옵니다.
# cpage를 순회합니다.
def get_comments(deal_no, driver, soup, comment_count):
    # 댓글 자체가 없는 글도 있음 ;;
    comments = []
    comments += parse_now_comments(deal_no, soup)
    try :
        if comment_count is not None:
            comment_page = math.ceil(comment_count / 50)
            for idx in range(2, comment_page+1):
                page_soup = get_cpage_soup(driver, deal_no, idx)
                comments += parse_now_comments(deal_no, page_soup)

        return comments

    except Exception as e:
        save_error_log(deal_no, "PARSE ERROR", f"{deal_no} : cant parse comment pages, {str(e)}")
        return []


# 현재 페이지의 코멘트들을 파싱해 반환합니다.
def parse_now_comments(deal_no, soup: BeautifulSoup):
    try :
        comments = []
        li_tags = soup.select("ul.fdb_lst_ul > li.fdb_itm")
        for li in li_tags:
            if "comment_best" in li.get("class", []):
                continue  # 베스트 댓글 제외

            content = get_content(deal_no, li)
            username = get_username(deal_no, li)
            upvote = get_upvote(deal_no, li)
            downvote = get_downvote(deal_no, li)


            created_at = parse_date_time(get_datetime(deal_no, li))

            if content and username:
                comments.append(CommentDTO(
                    deal_no=deal_no,
                    content=content,
                    username=username,
                    upvote=upvote,
                    downvote=downvote,
                    source_site=Site.FMKOREA,
                    created_at=created_at
                ))

    except Exception as e :
        save_error_log(deal_no, "PARSE ERROR",f"{deal_no} : cant parse comments, {str(e)}")
        return []

    return comments

def get_content(deal_no, li):
    try :
        return li.select_one("div.comment-content div.xe_content").get_text(strip=True)
    except Exception as e :
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get comment \n {str(e)}")
        return None


def get_username(deal_no, li):
    try:
        return li.select_one("a.member_plate").get_text(strip=True)
    except Exception as e:
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get comment user \n {str(e)}")
        return None

def get_upvote(deal_no, li):
    try:
        upvote = li.select_one("span.voted_count").get_text(strip=True)
        upvote = int(upvote) if upvote != '' else 0
        return upvote
    except Exception as e:
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get comment upvote \n {str(e)}")
        return None

def get_downvote(deal_no, li):
    try:
        downvote = li.select_one("span.blamed_count").get_text(strip=True)
        downvote = int(downvote) if downvote != '' else 0
        return downvote
    except Exception as e:
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get comment upvote \n {str(e)}")
        return None

def get_datetime(deal_no, li):
    try:
        return li.select_one("span.date").get_text(strip=True)
    except Exception as e:
        save_error_log(Site.FMKOREA, "PARSING ERROR", f"{deal_no} : can't get comment upvote \n {str(e)}")
        return None

def get_cpage_soup(driver, deal_no, comment_page) :
    driver.get(Site.FMKOREA.deal_detail_url + str(deal_no) + "?cpage=" + str(comment_page))
    from time import sleep
    sleep(1)
    html = driver.page_source
    return parse_html(html)