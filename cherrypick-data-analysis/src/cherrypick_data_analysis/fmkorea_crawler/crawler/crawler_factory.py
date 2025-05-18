import traceback
from time import sleep
from cherrypick_data_analysis.shared.enum import Site
from cherrypick_data_analysis.logic.crawler.modules import parse_fmkorea
from concurrent.futures import ThreadPoolExecutor

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
    global custom_parser
    if source_site == Site.FMKOREA :
        custom_parser = parse_fmkorea

    next_idx = int(start_no)
    while(True) :
        try :
            if cancel_flag[source_site] :
                print(source_site.name + " 크롤링이 종료되었습니다.")
                break

            # 파싱
            dto = custom_parser(driver, next_idx)
            next_idx = dto.next_page
            sleep(2)
        except Exception as e :
            traceback.print_exc()
    driver.quit()

def crawl_stop(source_site : Site) :
    cancel_flag[source_site] = True
