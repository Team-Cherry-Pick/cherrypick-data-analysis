import queue
import time
import traceback
from typing import List

from sqlalchemy.orm import Session
from unicodedata import category
from datetime import datetime
from shared.database.model import Comment
from shared.save_process.page_dto import UserDTO, PageDTO
from shared.enum.crawler_status import Status, DataKey
from shared.enum.site import Site
from shared.database.database import get_session
from shared.database.model.deal import Deal
from shared.database.model.user import User
from shared.util.openai_util import classify_deals
from shared.util.redis_util import set_crawler_data, save_error_log, get_crawler_status

TOTAL_COUNT = 0
FAILURE_COUNT = 0
QUEUE_COUNT = 0

def save_users(session:Session, site:Site, pages:List[PageDTO]):

    deal_comment_users = []
    for page in pages:
         deal_comment_users += page.users
    username_set = set(u.username for u in deal_comment_users)

    queried_user_list = session.query(User).filter(User.username.in_(username_set),
                               User.source_site == site.name
                               ).all()
    user_dict = {u.username: u for u in queried_user_list}

    for user in deal_comment_users:
        origin_user = user_dict.get(user.username)
        if origin_user is None:
            # noinspection PyTypeChecker
            origin_user = user_dict[user.username] = User(
                username=user.username,
                source_site=user.source_site.name,
                first_appear_time=user.appear_time,
                last_appear_time=user.appear_time
            )

        if origin_user.first_appear_time < user.appear_time :
            if  origin_user.last_appear_time < user.appear_time : origin_user.last_appear_time = user.appear_time
        else :
            if user.appear_time < origin_user.first_appear_time : origin_user.first_appear_time = user.appear_time

    try:
        session.add_all(user_dict.values())
        session.commit()
    except Exception as e:
        session.rollback()
        print("[RETRY] 1회 재시도")
        try:
            session.add_all(user_dict.values())  # 다시 add 필요
            session.commit()
        except Exception as e:
            session.rollback()
            raise

    return user_dict

def save_deals(session:Session, pages:List[PageDTO], user_dict:dict, category_dict:dict) :

    deals = [page.deal for page in pages]
    deal_dict = {int(deal.deal_no): Deal(
        source_site=deal.source_site.name,
        deal_no=deal.deal_no,
        user_id=user_dict[deal.username].user_id,
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
        category_id=category_dict[str(deal.deal_no)],
        created_at=deal.created_at
    ) for deal in deals}

    session.add_all(deal_dict.values())
    session.commit()

    return deal_dict

def save_comments(session:Session, pages, deal_dict:dict, user_dict:dict):
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
                user_id=user_dict[comment.username].user_id,
                created_at=comment.created_at
            ) for comment in comments]
    session.add_all(comment_for_save)
    session.commit()



def data_save_process(q : queue, source_site : Site):
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
                batch.append(q.get(timeout=timeout))
                q.task_done()
            except queue.Empty:
                break

        if not batch:
            continue  # 큐 비었고, 타임아웃됨

        try :
            print(f"START SAVING DATA {datetime.now()}")

            # 크롤러 상태 변수 초기화
            global TOTAL_COUNT
            TOTAL_COUNT += len(batch)
            set_crawler_data(source_site, DataKey.TOTAL_COUNT, TOTAL_COUNT)
            with q.mutex:
                set_crawler_data(source_site, DataKey.QUEUED_COUNT, len(q.queue))

            #########################
            ###      DB 저장
            #########################
            session = get_session()
            # USER 저장
            user_dict = save_users(session, source_site, batch)

            # DEAL 저장
            category_dict = get_category_dict(batch)
            deal_dict = save_deals(session, batch, user_dict, category_dict)

            # COMMENT 저장
            save_comments(session, batch, deal_dict, user_dict)

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


def get_category_dict(batch) :
    dict_list = [{
        "deal_no": dto.deal.deal_no,
        "title": dto.deal.title,
        "content": dto.deal.content,
    } for dto in batch]
    return classify_deals(dict_list)







