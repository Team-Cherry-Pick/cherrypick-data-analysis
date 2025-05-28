import sys

import requests

from cherrypick_data_analysis.shared.config.env import SLACK_URL
from cherrypick_data_analysis.shared.enum.site import Site
from shared.enum.crawler_status import DataKey
from shared.util.redis_util import get_crawler_data

WEB_HOOK_URL = SLACK_URL

def send_slack(text) :
    message = f"[{sys.argv[1]}]\n{text}"

    payload = {"attachments" : [{"text" : message}]} # 접기 기능 등 활성화
    requests.post(WEB_HOOK_URL, json=payload)

def init_message(site: Site) :
    send_slack(f"Crawler가 {site.name}에 잠입했습니다 . . . ! 😎😎😎\n 오늘은 {get_crawler_data(site, DataKey.NOW_CRAWLING)}p부터 신나게 긁어볼까요~!")

def block_message(site : Site, start_page, page) :
    send_slack(f"{site.name} 접근이 차단 당했습니다 😭😭😭 \n{start_page - page}p 페이지를 긁었습니다 ! \n 어슬렁 거리다가 6시간 뒤에 다시 잠입하겠습니다...😎")

def retry_message(site: Site) :
    send_slack(f"키키키 {site.name} 다시 접근해보겠습니다 😃😃😃")

def status_message(site : Site) :
    send_slack(f"""
키키키 ! {site.name} Crawler {get_crawler_data(site, DataKey.TOTAL_COUNT)}개 수집 성공 !!😎
[현재 상태]
평균 시간 : {get_crawler_data(site, DataKey.AVERAGE_DURATION)}
현재 페이지 : {get_crawler_data(site, DataKey.NOW_CRAWLING)}
마지막 저장 : {get_crawler_data(site, DataKey.LAST_SAVED_TIME)}
딜레이 타임 : 1s~{get_crawler_data(site, DataKey.DELAY_TIME)}
계속 수집하겠습니다 ! 😏 
    """)

def finalize_message(site : Site, start_page, page) :
    send_slack(f"🎉🎉🎉 {site.name} Crawler 성공적으로 종료했습니다 ! 🎉🎉🎉\n*{page - start_page}p* 페이지를 긁었습니다 !\n다음에는 *{page}p* 부터 시작하면 됩니다 !")