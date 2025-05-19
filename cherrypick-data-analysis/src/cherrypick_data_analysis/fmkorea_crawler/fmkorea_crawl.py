import threading
from datetime import datetime
from queue import Queue

from shared.database.database import engine, Base
from shared.enum.site import Site
from shared.util.crawl_util import get_driver
import time
from fmkorea_crawler.crawler.modules import parse_fmkorea
from shared.dto.data_save_process import data_save_process
from shared.util.redis_util import get_crawler_status, set_crawler_status, set_crawler_data, initialize_redis, \
    calculate_average_duration
from shared.enum.crawler_status import Status, DataKey

q = Queue()
Base.metadata.create_all(engine)
thread = threading.Thread(target=data_save_process, args=(q, Site.FMKOREA, )).start()

def crawl_start() :
    print("FMKOREA 크롤링 시작")
    initialize_redis(Site.FMKOREA)

    next_idx = 1254308182
    driver = get_driver()
    while (True):

        try :

            status = get_crawler_status(Site.FMKOREA)
            if status == Status.BREAK :
                print("FM Korea 크롤링 서비스를 중단합니다 . . .")
                break
            if status == Status.STOPPED :
                print("FM Korea 크롤링 서비스 RUNNING 명령까지 대기 중 . . .")
                time.sleep(5)
                continue

            set_crawler_data(Site.FMKOREA, DataKey.NOW_CRAWLING, next_idx)
            # 파싱
            dto = parse_fmkorea(driver, next_idx)
            if dto.next_page is None:
                set_crawler_status(Site.FMKOREA, Status.WAITING)
                print("FM Korea 크롤링 서비스 다음 글을 대기 중 . . .")
                time.sleep(60)
            else :
                next_idx = dto.next_page

            q.put(dto)
            time.sleep(1)

            avg_duration = calculate_average_duration(Site.FMKOREA)
            set_crawler_data(Site.FMKOREA, DataKey.AVERAGE_DURATION, avg_duration)
            set_crawler_data(Site.FMKOREA, DataKey.QUEUED_COUNT, q.qsize())

        except Exception as e:
            print(e)

    global thread

    driver.quit()






