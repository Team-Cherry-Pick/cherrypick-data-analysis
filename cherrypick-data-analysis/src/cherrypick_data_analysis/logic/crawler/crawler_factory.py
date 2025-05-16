from random import random
from time import sleep
from cherrypick_data_analysis.glob.enum.site import Site
from  cherrypick_data_analysis.logic.crawler.modules import fmkorea_parse
from concurrent.futures import ThreadPoolExecutor
from cherrypick_data_analysis.glob.util.crawl_util import *

executor = ThreadPoolExecutor(max_workers=5)  # 전역 스레드풀 생성

cancel_flag = {
    Site.FMKOREA : False,
    Site.PPOMPPU : False
               }

# 스레드풀에 크롤러 넣고 시작해줌.
def crawl_start(source_site : Site, start_no : int) :
    cancel_flag[source_site] = False
    executor.submit(crawl_process, source_site, start_no)


# 실제 크롤링 하는 녀석
def crawl_process(source_site : Site, start_no : int) :

    driver = get_driver()

    global base_url
    global parser
    if source_site == Site.FMKOREA :
        base_url = source_site.FMKOREA.deal_detail_url
        parser = fmkorea_parse

    idx = start_no
    #while(True) :
    driver.get(base_url+idx)
    print(base_url+idx)
    sleep(1)
    html = driver.page_source
    soup = parse_html(html)
    print(soup)
    sleep(random.randint(1,3))

def get_category(store) :
    return None

def crawl_store(link) :
    return None

