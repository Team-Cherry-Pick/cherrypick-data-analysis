from typing import List

from cherrypick_data_analysis.shared.database.database import get_session
from cherrypick_data_analysis.shared.database.model import Deal
import pandas as pd

from cherrypick_data_analysis.shared.enum.site import Site


def get_all_deal_no(deal_no_set) :
    session = get_session()
    deal_no_list = session.query(Deal.deal_no).filter(Deal.deal_no.in_(deal_no_set)).all()
    session.close()

    return {d[0] for d in deal_no_list}

def get_all_deals_show():
    session = get_session()
    deals = session.query(Deal).order_by(Deal.created_at.desc()).limit(100).all()

    df = pd.DataFrame([
        {
            "infos" : "|||||||||",
            "id": d.deal_id,
            "no": d.deal_no,
            "사이트": d.source_site.name if d.source_site else None,
            "제목": d.title,
            "내용": d.content,
            "values" : "|||||||||",
            "추천 수" : d.vote,
            "가격" : d.discounted_price,
            "단위" : d.price_type.name,
            "게시일" : d.created_at

        } for d in deals
    ])
    session.close()
    return df

def get_all_deals_dataframe():
    session = get_session()
    deals = session.query(Deal).order_by(Deal.created_at.desc()).all()

    df = pd.DataFrame([
        {
            "deal_id": d.deal_id,
            "deal_no": d.deal_no,
            "source_site": d.source_site.name if d.source_site else None,
            "title" : d.title,
            "content": d.content,
            "vote" : d.vote,
            "views" : d.views,
            "origin_price" : d.origin_price,
            "discounted_price" : d.discounted_price,
            "price_type" : d.price_type.name,
            "is_expired" : d.is_expired,
            "comment_count" : d.comment_count,
            "category_id" : d.category_id,
            "user_id" : d.user_id,
            "is_published" : d.is_published,
            "product_link" : d.product_link,
            "store" : d.store,
            "created_at" : d.created_at,
            "category_name" : d.category.name,
        } for d in deals
    ])
    session.close()

    return df

def get_deals_created_at(siteList:List[Site]) :
    session = get_session()
    deals = (session.query(Deal.created_at)
             .filter(Deal.source_site.in_(siteList))
             .order_by(Deal.created_at.desc())
             .all())

    df = pd.DataFrame([
        {
            "created_at" : d.created_at
        } for d in deals
    ])
    session.close()
    return df
