from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
from urllib.parse import urlparse

from fmkorea_crawler.crawler.page_dto import DealDTO, CommentDTO

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive',
}

options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # 브라우저 안 띄움
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=ko-KR')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/114.0.0.0 Safari/537.36")

def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def parse_html(content) :
    return BeautifulSoup(content, 'html.parser')

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
    print("└────────────────────────────────────┘")


def print_comment_dto(comment):
    print("┌───────────── CommentDTO ─────────────┐")
    print(f"│ username     : {comment.username}")
    print(f"│ created_at   : {comment.created_at}")
    print(f"│ upvote       : {comment.upvote}")
    print(f"│ downvote     : {comment.downvote}")
    print(f"│ content      : {comment.content[:80]}{'...' if len(comment.content) > 80 else ''}")
    print("└──────────────────────────────────────┘")

def extract_base_url(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception as e:
        print(f"[URL PARSE ERROR] {e}")
        return None


def parse_date_time(raw, default) :
    try :
        return datetime.strptime(raw, "%Y.%m.%d %H:%M")
    except Exception as e:
        print(f"[DATE PARSE ERROR] {e}")
        return default

import requests

def get_redirect_url(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        return extract_base_url(response.url)
    except requests.RequestException as e:
        print(f"[ERROR] URL 추적 실패: {e}")
        return None


def extract_price(text: str):
    try:
        digits = re.sub(r"[^\d]", "", text)
        return int(digits) if digits else None
    except Exception as e:
        print(f"[PRICE PARSE ERROR] {e}")
        return None

from datetime import datetime, timedelta
import re

def parse_relative_time(text: str) -> datetime:
    now = datetime.now()

    hour_match = re.search(r"(\d+)\s*시간 전", text)
    minute_match = re.search(r"(\d+)\s*분 전", text)

    if hour_match:
        hours = int(hour_match.group(1))
        return now - timedelta(hours=hours)
    elif minute_match:
        minutes = int(minute_match.group(1))
        return now - timedelta(minutes=minutes)
    else:
        return None  # 또는 예외 처리
