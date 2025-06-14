import queue
import time
import traceback
from datetime import datetime
from typing import List

from shared.enum.crawler_status import Status, DataKey
from shared.enum.site import Site
from shared.process.page_dto import PageDTO
from shared.util.openai_util import classify_deals
from shared.util.redis_util import get_crawler_status, set_crawler_data, save_error_log

TOTAL_COUNT = 0
FAILURE_COUNT = 0
QUEUE_COUNT = 0

def category_classify_process(input_q : queue, output_q : queue, source_site : Site):
    batch_size = 5
    timeout = 30

    while True:
        batch = []
        start = time.time()

        while len(batch) < batch_size and (time.time() - start) < timeout:
            # 멈춰!!
            status = get_crawler_status(source_site)
            if status == Status.BREAK:
                break
            try:
                batch.append(input_q.get(timeout=timeout))
            except queue.Empty:
                break

        if not batch:
            continue  # 큐 비었고, 타임아웃됨

        try :
            #print(f"START CATEGORY CLASSIFYING {datetime.now()}")
            category_dict = get_category_dict(batch)
            set_deal_category(batch, category_dict) # 이 과정을 거쳐 배치에는 카테고리가 심어짐
            for deal in batch:
                output_q.put(deal)

        except Exception as e:
            global FAILURE_COUNT
            traceback.print_exc()
            print(f"ERROR {e}")
            # 에러 저장
            save_error_log(source_site,"SAVE ERROR", e)
            # 에러난 애들 더해줌
            FAILURE_COUNT += len(batch)
            set_crawler_data(source_site, DataKey.FAILURE_COUNT, FAILURE_COUNT)


def get_category_dict(batch) :
    dict_list = [{
        "deal_no": dto.deal.deal_no,
        "title": dto.deal.title,
        "content": dto.deal.content,
    } for dto in batch]
    return classify_deals(dict_list)

def set_deal_category(pages:List[PageDTO], category_dict:dict) :

    deals = [page.deal for page in pages]
    for deal in deals :
        deal.category_id = category_dict[str(deal.deal_no)]

    return deals