import queue
import time
from typing import List

from unicodedata import category

from shared.database.model import Comment
from shared.dto.page_dto import UserDTO
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


def get_user_list(appear_user:List[UserDTO], user_dict:dict):
    #print("GET USER LIST")
    target_users = []
    for user in appear_user:
        origin_user = user_dict.get(user.username)
        if origin_user is None:
            origin_user = user_dict[user.username] = User(
                username=user.username,
                source_site=user.source_site.name,
                first_appear_time=user.appear_time,
                last_appear_time=user.appear_time
            )

        origin_user.last_appear_time = user.appear_time
        target_users.append(origin_user)

    return target_users



def get_deal_list(deal, user_dict:dict, category_dict:dict) :
    #print("GET DEAL LIST")

    return Deal(
        source_site=deal.source_site.name,
        deal_no=deal.deal_no,
        user_id=user_dict[deal.username].user_id,
        title=deal.title,
        content=deal.content,

        origin_price=deal.origin_price,
        discounted_price=deal.discounted_price,
        vote=deal.vote,
        views=deal.views,
        comment_count=deal.comment_count,
        is_expired=deal.is_expired,
        store=deal.store,
        product_link=deal.product_link,
        category_id=category_dict[str(deal.deal_no)],
        created_at=deal.created_at
    )

def get_comment_list(comments, deal_dict:dict, user_dict:dict):
    #print("GET COMMENT LIST")
    comment_list = []
    for comment in comments:
        comment_list.append(
            Comment(
                content=comment.content,
                up_vote=comment.upvote,
                down_vote=comment.downvote,
                source_site=comment.source_site.name,
                deal_id=deal_dict[int(comment.deal_no)].deal_id,
                user_id=user_dict[comment.username].user_id,
                created_at=comment.created_at
            )
        )
    return comment_list


def data_save_process(q : queue, source_site : Site):
    print("====SAVING DATA=====")
    batch_size = 5
    timeout = 20


    while True:
        batch = []
        start = time.time()
        session = get_session()

        while len(batch) < batch_size and (time.time() - start) < timeout:

            # 멈춰!!
            status = get_crawler_status(source_site)
            if status == Status.BREAK :
                break

            try:
                batch.append(q.get(timeout=timeout))
                q.task_done()
            except queue.Empty:
                break

        if not batch:
            continue  # 큐 비었고, 타임아웃됨

        try :
            global TOTAL_COUNT
            TOTAL_COUNT += len(batch)
            set_crawler_data(source_site, DataKey.TOTAL_COUNT, TOTAL_COUNT)
            set_crawler_data(source_site, DataKey.QUEUED_COUNT, q.qsize())

            users = session.query(User).filter(User.source_site == source_site.name).all()
            deals = session.query(Deal).filter(Deal.source_site == source_site.name).all()
            user_dict = {user.username: user for user in users}

            for dto in batch:
                if dto.deal.deal_no == next((d.deal_no for d in deals if d.deal_no == dto.deal.deal_no), None) :
                    batch.remove(dto)

            # USER
            appear_users = []
            for dto in batch:
                appear_users += get_user_list(dto.users, user_dict)

            session.add_all(appear_users)
            session.commit()
            user_dict = {user.username: user for user in appear_users}

            # DEAL
            dict_list = [{
                "deal_no": dto.deal.deal_no,
                "title": dto.deal.title,
                "content": dto.deal.content,
            } for dto in batch]

            category_dict = classify_deals(dict_list)
            new_deals = []
            for dto in batch:
                new_deals.append(get_deal_list(dto.deal, user_dict, category_dict))
            session.add_all(new_deals)
            session.commit()
            deal_dict = {deal.deal_no: deal for deal in new_deals}

            new_comments = []
            for dto in batch:
                new_comments += get_comment_list(dto.comments, deal_dict, user_dict)
            session.add_all(new_comments)
            session.commit()

            session.close()
        except Exception as e:
            global FAILURE_COUNT
            print(f"ERROR {e}")
            save_error_log(source_site,"SAVE ERROR", e)
            FAILURE_COUNT += len(batch)
            set_crawler_data(source_site, DataKey.FAILURE_COUNT, FAILURE_COUNT)










