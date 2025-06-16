import pandas as pd
from cherrypick_data_analysis.shared.database.database import get_session
from cherrypick_data_analysis.shared.database.model import Comment


def get_all_comment_dataframe() :
    session = get_session()
    comments = session.query(Comment).order_by(Comment.created_at).all()

    df = pd.DataFrame([
        {
            "comment_id" : comment.comment_id,
            "username" : comment.username,
            "source_site" : comment.source_site,
            "created_at" : comment.created_at,
            "deal_id" : comment.deal_id
        } for comment in comments
    ])

    return df

def get_comment_count() :
    session = get_session()
    session = get_session()
    from sqlalchemy import func
    result = session.query(Comment.source_site, func.count(Comment.comment_id)).group_by(Comment.source_site).all()
    return {r[0] : r[1] for r in result }