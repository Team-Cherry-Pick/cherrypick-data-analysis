import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

import requests

from shared.enum.price_type import PriceType
from shared.enum.site import Site
from shared.util.redis_util import save_error_log

# 상대 시간을 반환합니다.
# 없으면 None 입니다.
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

# 날짜를 규격에 맞게 파싱해줍니다.
# 만약 파싱 할 수 없는 문자열이라면, 상대 날짜를 구해 저장합니다 (14 분 전 등..)
# 그래도 안되면 그냥 None을 반홥합니다.
def parse_date_time(raw) :
    try :
        return datetime.strptime(raw, "%Y.%m.%d %H:%M")
    except Exception as e:
        return parse_relative_time(raw)

# 상품 링크에 직접 접속하여 해당 사이트의 탑레벨 도메인을 추출합니다.
# 알 수 없는 에러가 너무 많이 떠서 ...  그냥 레디스에는 안찍기로 했다.
# TO DO : 에러 해결
def get_store(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        from tldextract import tldextract
        ext = tldextract.extract(response.url)

        return ext.domain + '.' + ext.suffix
    except requests.RequestException as e:
        print(f"[ERROR] URL 추적 실패: {e}")
        return None

# origin 가격 문자열에서 가격 숫자를 추출합니다.
def extract_price(source_site:Site, deal_no, origin: str):
    try:
        # 1. 콤마 제거
        cleaned = origin.replace(",", "")

        # 2. 맨 앞이 숫자가 아니면 제거
        cleaned = re.sub(r"^\D+", "", cleaned)

        # 3. 숫자가 아닌 문자 기준으로 스플릿 → 첫 번째 숫자 조각 추출
        parts = re.split(r"\D+", cleaned)
        digits = parts[0] if parts and parts[0].isdigit() else None

        return int(digits) if digits else None

    except Exception as e:
        save_error_log(source_site, "PRICE PARSE ERROR",f"{deal_no} : cant extract price \n {str(e)}")
        return None


# origin 가격 문자열에서 가격 타입을 반환합니다.
# KRW, USD 를 반홥합니다..
def get_price_type(source_site:Site, deal_no, origin) :
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
        save_error_log(source_site, "PARSING ERROR",f"{deal_no} : cant extract price \n {str(e)}")
        return PriceType.KRW