import threading
from queue import Queue

from shared.database.database import engine, Base
from shared.enum.site import Site
from shared.util.crawl_util import get_driver
import time
from fmkorea_crawler.crawler.modules import parse_fmkorea
from shared.dto.data_save_process import data_save_process

q = Queue()
Base.metadata.create_all(engine)
threading.Thread(target=data_save_process, args=(q, Site.FMKOREA, )).start()


def crawl_start() :
    print("FMKOREA 크롤링 시작")

    next_idx = 1254308182
    driver = get_driver()
    while (True):

        try:
            # 파싱
            dto = parse_fmkorea(driver, next_idx)
            if dto.next_page is None:
                time.sleep(60)
            else :
                next_idx = dto.next_page

            q.put(dto)
            time.sleep(1)
        except Exception as e:
            print(e)

    driver.quit()





