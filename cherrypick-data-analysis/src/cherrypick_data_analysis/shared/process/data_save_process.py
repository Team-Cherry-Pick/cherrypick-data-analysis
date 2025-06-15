import queue
import time
import traceback
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from shared.database.model import Comment
from shared.process.page_dto import PageDTO
from shared.enum.crawler_status import Status, DataKey
from shared.enum.site import Site
from shared.database.database import get_session
from shared.database.model.deal import Deal
from shared.util.openai_util import classify_deals
from shared.util.redis_util import set_crawler_data, save_error_log, get_crawler_status

TOTAL_COUNT = 0
FAILURE_COUNT = 0
QUEUE_COUNT = 0

def save_deals(session:Session, pages:List[PageDTO]) :

    deals = [page.deal for page in pages]
    deal_dict = {int(deal.deal_no): Deal(
        source_site=deal.source_site.name,
        deal_no=deal.deal_no,
        username=deal.username,
        title=deal.title,
        content=deal.content,

        price_type=deal.price_type,
        origin_price=deal.origin_price,
        discounted_price=deal.discounted_price,
        vote=deal.vote,
        views=deal.views,
        comment_count=deal.comment_count,
        is_expired=deal.is_expired,
        is_blinded=deal.is_blinded,

        store=deal.store,
        product_link=deal.product_link,
        category_id=deal.category_id,
        created_at=deal.created_at
    ) for deal in deals}

    session.add_all(deal_dict.values())
    session.commit()

    return deal_dict

def save_comments(session:Session, pages, deal_dict:dict):
    #print("GET COMMENT LIST")
    comments = []
    for page in pages:
        comments += page.comments

    comment_for_save = [Comment(
                content=comment.content,
                up_vote=comment.upvote,
                down_vote=comment.downvote,
                source_site=comment.source_site.name,
                deal_id=deal_dict[int(comment.deal_no)].deal_id,
                username=comment.username,
                created_at=comment.created_at
            ) for comment in comments]
    session.add_all(comment_for_save)
    session.commit()



def data_save_process(q, source_site : Site, batch_size=5):
    timeout =30

    while True:
        batch = []
        start = time.time()

        while len(batch) < batch_size and (time.time() - start) < 60:
            # 멈춰!!x
            status = get_crawler_status(source_site)
            if status == Status.BREAK:
                break
            try:
                batch.append(q.get(timeout=timeout))
            except queue.Empty:
                break

        if not batch:
            continue  # 큐 비었고, 타임아웃됨

        try :
            print(f"START SAVING DATA {datetime.now()}")
            save_error_log(source_site, "test", f"{len(batch)}")
            # 크롤러 상태 변수 초기화
            global TOTAL_COUNT
            TOTAL_COUNT += len(batch)
            set_crawler_data(source_site, DataKey.TOTAL_COUNT, TOTAL_COUNT)

            #########################
            ###      DB 저장
            #########################
            session = get_session()

            # DEAL 저장
            deal_dict = save_deals(session, batch)

            # COMMENT 저장
            save_comments(session, batch, deal_dict)

            session.close()
            set_crawler_data(source_site, DataKey.LAST_SAVED_TIME, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            global FAILURE_COUNT
            traceback.print_exc()
            print(f"ERROR {e}")
            # 에러 저장
            save_error_log(source_site,"SAVE ERROR", e)
            # 에러난 애들 더해줌
            FAILURE_COUNT += len(batch)
            set_crawler_data(source_site, DataKey.FAILURE_COUNT, FAILURE_COUNT)







