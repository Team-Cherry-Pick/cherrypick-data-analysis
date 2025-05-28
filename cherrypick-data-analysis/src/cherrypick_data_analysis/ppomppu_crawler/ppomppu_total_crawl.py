import threading
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver

from fmkorea_crawler.fmkorea_total_crawl import get_new_links
from shared.database.database import *
from shared.query.raw_query import get_all_page_no
from shared.util import slack_util
from shared.util.crawl_util import get_driver, parse_html
from shared.util.redis_util import *
import shared.util.slack_util as slack

def crawl_start(start_page) :
    print("PPOMPPU 크롤링 시작")
    initialize_redis(Site.PPOMPPU)

    Base.metadata.create_all(engine)

    page = start_page
    if page == -1 :
        page = get_start_page(Site.PPOMPPU)

    phase = 1 # 500개 크롤링 할때마다 phase가 1 증가
    driver = get_driver()
    slack.init_message(Site.PPOMPPU)
    while True:
        # 현재 크롤링 중인 페이지를 알림.
        set_crawler_data(Site.PPOMPPU, DataKey.NOW_CRAWLING, page)
        # 현재 페이지에서 크롤링 해야할 링크 선별
        # 중복 저장 방지
        links = get_new_links(driver, page)
        for link in links :


        page += 1
        sleep(1)



# 링크가 아예 없을수도 있음. 그러면 오류
def get_main_list(driver:WebDriver, page) :
    try :
        driver.get(Site.PPOMPPU.deal_list_url + str(page))
        sleep(1)
        soup = parse_html(driver.page_source)
        links = soup.find_all('td', class_=['baseList-space', 'baseList-numb'])

        # 필터링 (두 클래스 모두 포함하는 경우만)
        links = [tag for tag in links if 'baseList-space' in tag['class'] and 'baseList-numb' in tag['class']]
        if len(links) <= 0 :
            raise Exception("no links")

        results = {link.text.strip() for link in links}
        return results
    except Exception as e:
        save_error_log(Site.PPOMPPU, "LIST ERROR", f"cant get list, {str(e)}")
        return None

def get_new_links(driver:WebDriver, page) :
    try :
        # 이미 저장된 핫딜을 배제하는 과정
        links = get_main_list(driver, page)
        exist_link_set = get_all_page_no(links, Site.PPOMPPU)
        links = links - exist_link_set
        return links
    except Exception as e :
        save_error_log(Site.FMKOREA, "LIST ERROR", f"cant get new list, {str(e)}")
        return None