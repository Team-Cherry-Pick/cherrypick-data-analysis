# 크롤링 하는 본체
from queue import Queue

from selenium.webdriver.chrome.webdriver import WebDriver
from cherrypick_data_analysis.shared.enum.site import Site
from cherrypick_data_analysis.shared.util.redis_util import initialize_redis, get_start_page, set_crawler_data, save_error_log
from cherrypick_data_analysis.shared.util.crawl_util import get_driver, parse_html
import cherrypick_data_analysis.shared.util.slack_util as slack
from cherrypick_data_analysis.shared.enum.crawler_status import DataKey
from time import sleep

from fmkorea_crawler.crawler.modules import parse_fmkorea

task_queue = Queue()

def crawl_latest_deals():
    print("FMKOREA 최신 글 크롤링 시작")
    initialize_redis(Site.FMKOREA)

    page = 1

    driver = get_driver()
    slack.send_slack(f"Crawler가 {Site.FMKOREA.name}에 잠입했습니다 . . . !")

    while True:
        # 중복 저장 방지
        deals = get_main_list(driver, page) # (deal_id, store_name)
        for deal in deals :
            deal_id, store_name = deal[0], deal[1]
            if store_name in "지마켓/쿠팡와우/롯데온/옥션/11번가" :
                data = parse_fmkorea(driver, int(deal_id))
                print(data)

                sleep(600)
        break


    print("cancel crawling . . .")
    driver.quit()


# 링크가 아예 없을수도 있음. 그러면 오류
def get_main_list(driver:WebDriver, page) :
    try :
        driver.get(Site.FMKOREA.deal_list_url + str(1))
        sleep(1)
        soup = parse_html(driver.page_source)

        results = []
        for li in soup.select("li.li"):  # li 태그 중 class="li"인 것들 전부
            # 글 번호
            link = li.select_one("h3.title a")
            if not link:
                continue
            post_id = link["href"].strip("/")

            # 쇼핑몰
            shop_tag = li.select_one("div.hotdeal_info span a")
            shop_name = shop_tag.get_text(strip=True) if shop_tag else None

            results.append((post_id, shop_name))
        return results

    except Exception as e:
        save_error_log(Site.FMKOREA, "LIST ERROR", f"cant get list, {str(e)}")
        return None


def get_new_links(driver:WebDriver, page) :
    pass