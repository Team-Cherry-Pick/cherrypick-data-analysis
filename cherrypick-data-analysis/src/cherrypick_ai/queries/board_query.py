from sqlalchemy.orm import Session
from src.cherrypick_ai.models.board import Board# 모델 불러오기
from src.cherrypick_ai.models.hash_tag import HashTag # 모델 불러오기
from src.cherrypick_ai.database import get_session  # DB 엔진 불러오기

# ✅ 세션 생성
session = get_session()


def get_hashtags_for_board(board_id : int):

    # ✅ 특정 게시글을 가져오고, 연결된 해시태그를 조회
    board = session.query(Board).filter(Board.board_id == board_id).first()

    if board:
        return [tag.tag_id for tag in board.hash_tags]  # 해시태그 리스트 반환
    else:
        return None  # 게시글이 존재하지 않으면 None 반환



