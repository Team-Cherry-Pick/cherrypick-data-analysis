import queue
import threading

from ppomppu_crawler.parser.page_parser import parse_ppomppu
from shared.database.database import get_session
from shared.database.model import RawPage
from shared.enum.site import Site
from datetime import datetime

from shared.process.category_classify_process import category_classify_process
from shared.process.data_save_process import data_save_process
from shared.util.crawl_util import parse_html


site = Site.PPOMPPU
category_q = queue.Queue()
saving_q = queue.Queue()

def parse_all():
    session = get_session()
    cnt = 0

    try:
        for row in session.query(RawPage.page_no, RawPage.raw_html).yield_per(100):
            page_no, raw_html = row.page_no, row.raw_html
            # 실제 파싱 처리
            category_q.put(parse_ppomppu(page_no, parse_html(raw_html)))
            cnt += 1
            if cnt % 100 == 0:
                print(f"{datetime.now()} : {cnt}건 처리 완료")
    finally:
        session.close()


print(datetime.now())


for _ in range(5): threading.Thread(target=category_classify_process, args=(category_q, saving_q, site,)).start()
threading.Thread(target=data_save_process, args=(saving_q, site,)).start()

parse_all()
print(datetime.now())