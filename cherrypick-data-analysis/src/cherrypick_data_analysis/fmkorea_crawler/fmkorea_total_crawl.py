import math
import threading
from queue import Queue
from selenium.webdriver.chrome.webdriver import WebDriver

from fmkorea_crawler.crawler.modules import parse_fmkorea
from shared.database.database import engine, Base
import random
from shared.query.deal_query import get_all_deal_no
from shared.util.crawl_util import get_driver, parse_html
from shared.save_process.data_save_process import data_save_process
from shared.util.redis_util import *
from time import sleep

import shared.util.slack_util as slack

q = Queue()
# 크롤링 하는 본체
def crawl_start(start_page):
    print("FMKOREA 크롤링 시작")
    initialize_redis(Site.FMKOREA)

    Base.metadata.create_all(engine)
    threading.Thread(target=data_save_process, args=(q, Site.FMKOREA,)).start()


    page = start_page
    if page == -1 :
        page = get_start_page(Site.FMKOREA)


    phase = 1 # 500개 크롤링 할때마다 phase가 1 증가
    driver = get_driver()
    slack.send_slack(f"Crawler가 {Site.FMKOREA.name}에 잠입했습니다 . . . ! 😎😎😎\n 오늘은 {page}p부터 긁어볼까요~!")
    while True:
        # 현재 크롤링 중인 페이지를 알림.
        set_crawler_data(Site.FMKOREA, DataKey.NOW_CRAWLING, page)
        # 현재 페이지에서 크롤링 해야할 링크 선별
        # 중복 저장 방지
        links = get_new_links(driver, page)

        # 링크 받아오는 과정에서 오류가 나면 None, 이후 break
        if links is None :
            set_crawler_status(Site.FMKOREA, Status.WAITING)
            slack.block_message(Site.FMKOREA, start_page, page)
            sleep(14400)
            slack.retry_message(Site.FMKOREA)
            continue

        # 해당 링크들 순회하며 dto로 만들어 queue에 담음
        for link in links:
            q.put(parse_fmkorea(driver, int(link)))
            delay = int(get_crawler_data(Site.FMKOREA, DataKey.DELAY_TIME))
            sleep(random.randint(1, delay))

        # 만약 break라면 터뜨림
        if get_crawler_status(site=Site.FMKOREA) == Status.BREAK:
            break
        while get_crawler_status(site=Site.FMKOREA) == Status.STOPPED:
            sleep(1)
        set_crawler_status(site=Site.FMKOREA, status=Status.RUNNING)

        avg_duration = calculate_average_duration(Site.FMKOREA)
        set_crawler_data(Site.FMKOREA, DataKey.AVERAGE_DURATION, avg_duration)
        page+=1

        total = int(get_crawler_data(Site.FMKOREA, DataKey.TOTAL_COUNT))
        if 500 * phase < total :
            slack.status_message(Site.FMKOREA)
            driver.quit()
            driver = get_driver()
            phase += 1

    print("cancel crawling . . .")
    slack.finalize_message(Site.FMKOREA, start_page, page)
    driver.quit()



# 링크가 아예 없을수도 있음. 그러면 오류
def get_main_list(driver:WebDriver, page) :
    try :
        driver.get(Site.FMKOREA.deal_list_url + str(page))
        sleep(1)
        soup = parse_html(driver.page_source)
        links = soup.select("div.fm_best_widget._bd_pc a")
        hrefs = {int(a['href'][1:]) for a in links if 'href' in a.attrs and a['href'].startswith('/') and a['href'][1:].isdigit()}
        if len(hrefs) <= 0 :
            raise Exception("no links")

        return hrefs
    except Exception as e:
        save_error_log(Site.FMKOREA, "LIST ERROR", f"cant get list, {str(e)}")
        return None


def get_new_links(driver:WebDriver, page) :
    try :
        # 이미 저장된 핫딜을 배제하는 과정
        links = get_main_list(driver, page)
        exist_link_set = get_all_deal_no(links)
        links = links - exist_link_set
        return links
    except Exception as e :
        save_error_log(Site.FMKOREA, "LIST ERROR", f"cant get new list, {str(e)}")
        return None