import math

from selenium.webdriver.ie.webdriver import WebDriver
from time import sleep
from cherrypick_data_analysis.shared.util.crawl_util import *
from fmkorea_crawler.crawler.page_dto import DealDTO, CommentDTO
from shared.enum.site import Site
from datetime import datetime
from bs4 import BeautifulSoup

def parse_fmkorea(driver: WebDriver, deal_no):
    driver.get(Site.FMKOREA.deal_detail_url + str(deal_no) + "?cpage=1")
    sleep(1)
    html = driver.page_source
    from shared.util.crawl_util import parse_html
    soup = parse_html(html)

    try:
        print("FM_KOREA PARSE")
        source_site = Site.FMKOREA

        next_page = SAFE(deal_no, lambda: str(soup.select_one("a#auto_next_button").get("href")).replace("/", ""))

        username = SAFE(deal_no, lambda: soup.select_one("a.member_plate").get_text(strip=True))
        title = SAFE(deal_no, lambda: soup.select_one("h1.np_18px > span.np_18px_span").get_text(strip=True))
        content = SAFE(deal_no, lambda: soup.select_one("article").get_text(strip=True))

        discounted_price = SAFE(deal_no, lambda: extract_price(
            soup.find("th", string="가격").find_next_sibling("td").get_text(strip=True))
        )
        product_link = SAFE(deal_no, lambda: soup.select_one("td div.xe_content a").get("href"))
        store = SAFE(deal_no, lambda: get_redirect_url(product_link))

        info_box = soup.select("div.side.fr b")
        views = SAFE(deal_no, lambda: int(info_box[0].get_text(strip=True)))
        vote = SAFE(deal_no, lambda: int(info_box[1].get_text(strip=True)))
        comment_count = SAFE(deal_no, lambda: int(info_box[2].get_text(strip=True)))

        is_expired = SAFE(deal_no, lambda: soup.select_one("div.hotdeal_var8Y_msg") is not None)
        created_at = SAFE(deal_no, lambda: parse_date_time(
            soup.select_one("span.date.m_no").get_text(strip=True), default=None
        ))

        comments = parse_comment(deal_no, soup)
        comment_page = math.ceil(comment_count / 50)
        for idx in range(2, comment_page+1):
            page_soup = get_Comment_page_HTML(deal_no, idx, driver)
            comments += parse_comment(deal_no, page_soup)

        response = DealDTO(
            source_site=source_site,
            next_page=next_page,
            deal_no=deal_no,
            username=username,
            title=title,
            content=content,
            origin_price=None,
            discounted_price=discounted_price,
            vote=vote,
            views=views,
            comment_count=comment_count,
            is_expired=is_expired,
            store=store,
            product_link=product_link,
            created_at=created_at,
            comment_list=comments,
        )

        print_deal_dto(response)
        return response

    except Exception as e:
        print(f"[PARSING ERROR - {deal_no}] {e}")
        return None

def SAFE(deal_no, fn):
    try:
        return fn()
    except Exception as e:
        print(f"[ERROR - {deal_no}] {e}")
        return None

def parse_comment(deal_no, soup: BeautifulSoup):
    comments = []
    li_tags = soup.select("ul.fdb_lst_ul > li.fdb_itm")
    for li in li_tags:
        if "comment_best" in li.get("class", []):
            continue  # 베스트 댓글 제외

        content = SAFE(deal_no, lambda: li.select_one("div.comment-content div.xe_content").get_text(strip=True))
        username = SAFE(deal_no, lambda: li.select_one("a.member_plate").get_text(strip=True))

        upvote = SAFE(deal_no, lambda: li.select_one("span.voted_count").get_text(strip=True))
        upvote = int(upvote) if upvote != '' else 0
        downvote = SAFE(deal_no, lambda: li.select_one("span.blamed_count").get_text(strip=True))
        downvote = int(downvote) if downvote != '' else 0

        created_at = SAFE(deal_no, lambda: parse_relative_time(
            li.select_one("span.date").get_text(strip=True)
        ))

        if content and username:
            comments.append(CommentDTO(
                content=content,
                username=username,
                upvote=upvote,
                downvote=downvote,
                created_at=created_at
            ))
    return comments

def get_Comment_page_HTML(deal_no, comment_page : int, driver) :
    driver.get(Site.FMKOREA.deal_detail_url + str(deal_no) + "?cpage=" + str(comment_page))
    sleep(1)
    html = driver.page_source
    from shared.util.crawl_util import parse_html
    return parse_html(html)