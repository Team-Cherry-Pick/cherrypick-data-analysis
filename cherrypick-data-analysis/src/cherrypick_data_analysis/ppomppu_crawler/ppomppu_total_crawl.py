import random
import threading
from time import sleep

from narwhals import Datetime
from selenium.webdriver.chrome.webdriver import WebDriver

from ppomppu_crawler.crawler.crawler import get_raw_page_include_comments
from shared.database.database import *
from shared.database.model import RawPage
from shared.query.raw_query import get_all_page_no
from shared.util import slack_util
from shared.util.crawl_util import get_driver, parse_html
from shared.util.redis_util import *
import shared.util.slack_util as slack

site = Site.PPOMPPU


def crawl_start(start_page) :
    print("PPOMPPU 크롤링 시작")
    initialize_redis(site)

    Base.metadata.create_all(engine)

    count = 0
    page = start_page
    if page == -1 :
        page = get_start_page(site)

    phase = 1 # 500개 크롤링 할때마다 phase가 1 증가
    driver = get_driver()
    slack.init_message(site)
    while True:
        # 현재 크롤링 중인 페이지를 알림.
        set_crawler_data(site, DataKey.NOW_CRAWLING, page)
        # 현재 페이지에서 크롤링 해야할 링크 선별
        # 중복 저장 방지
        nos = get_new_nos(driver, page)
        
        # 링크 받아오는 과정에서 오류가 나면 None, 이후 break
        if nos is None :
            set_crawler_status(site, Status.WAITING)
            slack.block_message(site, start_page, page)
            sleep(14400)
            slack.retry_message(site)
            continue
        
        session = get_session()
        for no in nos :
            print(f"PPOMPPU PARSE : {datetime.now()}")
            html = get_raw_page_include_comments(driver, no)
            raw_page = RawPage(
                page_no=no,
                raw_html=html,
                created_at=datetime.now(),
                source_site=site.name,
            )
            count += 1
            set_crawler_data(site, DataKey.TOTAL_COUNT, count)
            set_crawler_data(site, DataKey.LAST_SAVED_TIME, datetime.now())
            session.add(raw_page)
            sleep(random.randint(1, int(get_crawler_data(site, DataKey.DELAY_TIME))))

        session.commit()

        # 만약 break라면 터뜨림
        if get_crawler_status(site=site) == Status.BREAK:
            break
        while get_crawler_status(site=site) == Status.STOPPED:
            sleep(1)
        set_crawler_status(site=site, status=Status.RUNNING)

        avg_duration = calculate_average_duration(site)
        set_crawler_data(site, DataKey.AVERAGE_DURATION, avg_duration)
        page += 1

        total = int(get_crawler_data(site, DataKey.TOTAL_COUNT))
        if 500 * phase < total:
            slack.status_message(site)
            driver.quit()
            driver = get_driver()
            phase += 1


    print("cancel crawling . . .")
    slack.finalize_message(site, start_page, page)
    driver.quit()
    page += 1
    sleep(random.randint(1, int(get_crawler_data(site, DataKey.DELAY_TIME))))



# 링크가 아예 없을수도 있음. 그러면 오류
def get_main_list(driver:WebDriver, page) :
    try :
        driver.get(site.deal_list_url + str(page))
        sleep(1)
        soup = parse_html(driver.page_source)
        nos = soup.find_all('td', class_=['baseList-space', 'baseList-numb'])

        # 필터링 (두 클래스 모두 포함하는 경우만)
        nos = [tag for tag in nos if 'baseList-space' in tag['class'] and 'baseList-numb' in tag['class']]
        if len(nos) <= 0 :
            raise Exception("no nos")

        results = {no.text.strip() for no in nos}
        return results
    except Exception as e:
        save_error_log(site, "LIST ERROR", f"cant get list, {str(e)}")
        return None

def get_new_nos(driver:WebDriver, page) :
    try :
        # 이미 저장된 핫딜을 배제하는 과정
        nos = get_main_list(driver, page)
        exist_no_set = get_all_page_no(nos, site)
        nos = nos - exist_no_set
        return nos
    except Exception as e :
        save_error_log(site, "LIST ERROR", f"cant get new list, {str(e)}")
        return None