import os
from multiprocessing import Process, Queue, current_process, freeze_support
from ppomppu_crawler.parser.page_parser import parse_ppomppu
from shared.database.database import get_session
from shared.database.model import RawPage
from shared.enum.site import Site
from datetime import datetime
from shared.process.category_classify_process import category_classify_process
from shared.process.data_save_process import data_save_process
from shared.util.crawl_util import parse_html
from time import sleep

site = Site.PPOMPPU
parsing_q = Queue()
category_q = Queue()
saving_q = Queue()

def load_process(output_q: Queue):
    session = get_session()
    cnt = 0
    try:
        for row in session.query(RawPage.page_no, RawPage.raw_html).filter(RawPage.raw_html.isnot(None)).yield_per(10):
            output_q.put((row.page_no, parse_html(row.raw_html)))
            cnt += 1
            if cnt % 100 == 0:
                print(f"{datetime.now()} : {cnt}건 로드 완료")

            if output_q.qsize() > 100 :
                sleep(1)

    finally:
        session.close()

def parse_process(input_q: Queue, output_q: Queue):
    while True:
        try:
            no, raw_html = input_q.get(timeout=100)
            result = parse_ppomppu(no, raw_html)
            output_q.put(result)
        except Exception:
            break

if __name__ == '__main__':
    freeze_support()  # Windows 대응

    print(datetime.now())

    workers = []

    print(os.cpu_count())  # 예: 8
    # 로드 먼저 수행
    print(f"로더 시작")
    loader = Process(target=load_process, args=(parsing_q,))
    loader.start()
    workers.append(loader)

    for _ in range(8):
        print(f"파서 멀티 프로세스 {_}")
        p = Process(target=parse_process, args=(parsing_q, category_q))
        p.start()
        workers.append(p)

    for _ in range(6):
        print(f"카테고리 멀티 프로세스 {_}")
        p = Process(target=category_classify_process, args=(category_q, saving_q, site))
        p.start()
        workers.append(p)

    print(f"데이터 저장 멀티 프로세스")
    saver = Process(target=data_save_process, args=(saving_q, site))
    saver.start()
    workers.append(saver)

    for p in workers:
        p.join()

    print(datetime.now())
