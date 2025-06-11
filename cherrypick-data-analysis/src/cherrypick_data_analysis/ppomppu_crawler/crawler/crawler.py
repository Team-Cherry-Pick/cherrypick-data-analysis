from time import sleep
from ppomppu_crawler.parser.page_parser import get_comment_count
from selenium.webdriver.chrome.webdriver import WebDriver
from random import randint

from shared.enum.crawler_status import DataKey
from shared.util.crawl_util import parse_html
from shared.enum.site import Site
from shared.util.redis_util import get_crawler_data, save_error_log


def get_raw_page_include_comments(driver:WebDriver, no) :
    try :
        driver.get(Site.PPOMPPU.deal_detail_url + str(no))
        total_html = html = driver.page_source
        soup = parse_html(html)

        # 코멘트 개수
        comment_count = get_comment_count(soup, no)
        for i in range(2, comment_count + 1) :
            driver.get(f"https://www.ppomppu.co.kr/zboard/comment.php?id=ppomppu&no={str(no)}&c_page={str(i)}")
            comments = driver.page_source
            total_html += comments

            sleep(randint(1, int(get_crawler_data(Site.PPOMPPU, DataKey.DELAY_TIME))))

        return total_html
    except Exception as e:
        save_error_log(Site.PPOMPPU, "GET RAW PAGE ERROR", {"message" : e, "no" : no})

