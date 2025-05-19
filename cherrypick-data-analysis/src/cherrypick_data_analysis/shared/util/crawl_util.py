import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

from shared.dto.page_dto import DealDTO
from shared.enum.price_type import PriceType

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
options.add_argument('--headless')  # 브라우저 안 띄움
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
        return parse_relative_time(raw)

import requests

def get_redirect_url(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        return extract_base_url(response.url)
    except requests.RequestException as e:
        print(f"[ERROR] URL 추적 실패: {e}")
        return None


import re


def extract_price(text: str):
    try:
        # 1. 콤마 제거
        cleaned = text.replace(",", "")

        # 2. 맨 앞이 숫자가 아니면 제거
        cleaned = re.sub(r"^\D+", "", cleaned)

        # 3. 숫자가 아닌 문자 기준으로 스플릿 → 첫 번째 숫자 조각 추출
        parts = re.split(r"\D+", cleaned)
        digits = parts[0] if parts and parts[0].isdigit() else None

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

def get_price_type(deal_no, origin) :
    try :
        patterns = [
            r'\$\s*\d+',                             # $123
            r'\d+(\.\d+)?\s*\$',                     # 123$
            r'\d+(\.\d+)?\s*(USD|usd|Usd)',          # 123 USD
            r'(USD|usd|Usd)\s*\d+(\.\d+)?',          # USD 123
            r'\d+(\.\d+)?\s*(달러|불)',              # 123달러
            r'(달러|불)\s*\d+(\.\d+)?',              # 달러123
            r'미화\s*\d+(\.\d+)?',                   # 미화 123
            r'\d+\s*달러\s*\d+\s*센트',              # 123달러 45센트
            r'\d+불',                                # 99불
            r'\bbucks\b',                            # bucks
            r'\b\d+\.\d{2}\b'                        # 123.99
        ]
        for pattern in patterns:
            if re.search(pattern, origin):
                return PriceType.USD
        return PriceType.KRW
    except Exception as e:
        traceback.print_exc()
        return PriceType.KRW