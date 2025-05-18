from shared.util.crawl_util import get_driver
from shared.enum.site import Site
from time import sleep
from fmkorea_crawler.crawler.modules import parse_fmkorea

page_queue = Queue()

def crawl_start() :
    print("FMKOREA 크롤링 시작")

    next_idx = int(input("시작할 번호를 입력해주세요."))
    driver = get_driver()
    while (True):

        try:
            # 파싱
            dto = parse_fmkorea(driver, next_idx)
            if dto.next_page is None:
                sleep(60)
            else :
                next_idx = dto.next_page

            sleep(1)
        except Exception as e:
            print(e)

    driver.quit()



