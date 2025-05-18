from selenium.webdriver.ie.webdriver import WebDriver
from time import sleep
from cherrypick_data_analysis.shared.enum import Site
from cherrypick_data_analysis.logic.crawler.page_dto import DealDTO
from cherrypick_data_analysis.shared.util import parse_html
from datetime import datetime
import re
from urllib.parse import urlparse

def SAFE(deal_no, fn):
    try:
        return fn()
    except Exception as e:
        print(f"[ERROR - {deal_no}] {e}")
        return None

def parse_fmkorea(driver: WebDriver, deal_no):
    driver.get(Site.FMKOREA.deal_detail_url + str(deal_no) + "?cpage=1")
    sleep(1)
    html = driver.page_source
    soup = parse_html(html)

    try:
        print("FM_KOREA PARSE")

        source_site = Site.FMKOREA
        next_page = SAFE(deal_no, lambda: str(soup.select_one("span.btn_pack.next.blockfmcopy a").get("href")).replace("/", ""))
        username = SAFE(deal_no, lambda: soup.select_one("a.member_plate").get_text(strip=True))
        title = SAFE(deal_no, lambda: soup.select_one("h1.np_18px > span.np_18px_span").get_text(strip=True))
        content = SAFE(deal_no, lambda: soup.select_one("article").get_text(strip=True))
        discounted_price = SAFE(deal_no, lambda: extract_price(soup.find("th", string="가격").find_next_sibling("td").get_text(strip=True)))
        product_link = SAFE(deal_no, lambda: soup.select_one("td div.xe_content a").get("href"))
        store = SAFE(deal_no, lambda: get_redirect_url(product_link))

        info_box = soup.select("div.side.fr b")
        views = SAFE(deal_no, lambda: int(info_box[0].get_text(strip=True)))
        vote = SAFE(deal_no, lambda: int(info_box[1].get_text(strip=True)))
        comment_count = SAFE(deal_no, lambda: int(info_box[2].get_text(strip=True)))

        is_expired = SAFE(deal_no, lambda: soup.select_one("div.hotdeal_var8Y_msg") is not None)
        created_at = SAFE(deal_no, lambda: parse_date_time(soup.select_one("span.date.m_no").get_text(strip=True)))

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
            comment_list=None,
        )

        print_deal_dto(response)
        return response

    except Exception as e:
        print(f"[PARSING ERROR - {deal_no}] {e}")
        return None



def print_deal_dto(dto: DealDTO):
    print("┌───────────── DealDTO ─────────────┐")
    print(f"│ site           : {dto.source_site}")
    print(f"│ deal_no        : {dto.deal_no}")
    print(f"│ next_page      : {dto.next_page}")
    print(f"│ username       : {dto.username}")
    print(f"│ title          : {dto.title}")
    print(f"│ content        : {dto.content[:80]}." if dto.content else "│ content        : None")
    print(f"│ product_link   : {dto.product_link}")
    print(f"│ store          : {dto.store}")
    print(f"│ vote           : {dto.vote}")
    print(f"│ views          : {dto.views}")
    print(f"│ origin_price   : {dto.origin_price}")
    print(f"│ discounted_price: {dto.discounted_price}")
    print(f"│ created_at     : {dto.created_at}")
    print(f"│ comment_list   : {dto.comment_list}")
    print("└────────────────────────────────────┘")


def extract_base_url(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception as e:
        print(f"[URL PARSE ERROR] {e}")
        return None


def parse_date_time(raw) :
    try :
        return datetime.strptime(raw, "%Y.%m.%d %H:%M")
    except Exception as e:
        print(f"[DATE PARSE ERROR] {e}")
        return None

import requests

def get_redirect_url(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        return extract_base_url(response.url)
    except requests.RequestException as e:
        print(f"[ERROR] URL 추적 실패: {e}")
        return None


def extract_price(text: str) -> int:
    try:
        digits = re.sub(r"[^\d]", "", text)
        return int(digits) if digits else None
    except Exception as e:
        print(f"[PRICE PARSE ERROR] {e}")
        return None