
from src.cherrypick_ai.database import get_session, engine  # DB 엔진 불러오기
from sqlalchemy import text

from src.cherrypick_ai.models.hash_tag import HashTag

# ✅ 세션 생성
session = get_session()

def get_tags_count():

    sql = text("select h.*, count(*) from hash_tag h inner join board_hashtag bh on h.tag_id = bh.tag_id group by h.tag_id;")
    with engine.connect() as conn:
        result = conn.execute(sql)
        rows = result.fetchall()

    filtered_rows = list(b[0] for b in rows if b[2]>30)
    return filtered_rows

def get_board_by_tag(tag_id):
    # ✅ 특정 게시글을 가져오고, 연결된 해시태그를 조회
    boards = list(h.boards for h in session.query(HashTag).filter(HashTag.tag_id==tag_id).all())

    return boards

