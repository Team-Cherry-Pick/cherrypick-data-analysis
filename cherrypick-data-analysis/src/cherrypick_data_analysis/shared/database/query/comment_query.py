from datetime import datetime
import pandas as pd
from sqlalchemy import func

from cherrypick_data_analysis.shared.database.database import get_session, get_engine
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

# 유저 당 쓴 글의 deal_count / views
def get_total_comment_user(start_date, end_date) :
    session = get_session()
    result = (session.query(Comment.username,
                            Comment.source_site,
                            func.count().label('comment_count'),
                            func.sum(Comment.up_vote).label('comment_upvote'),
                            func.sum(Comment.down_vote).label('comment_downvote'))
              .group_by(Comment.username, Comment.source_site)
              .filter(start_date <= Comment.created_at, Comment.created_at <= end_date)
              .all())
    return result
