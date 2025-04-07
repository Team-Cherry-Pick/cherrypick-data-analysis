from sklearn.feature_extraction.text import TfidfVectorizer

from src.cherrypick_ai.queries.hash_tag_query import *
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from src.cherrypick_ai.config.redis_config import get_redis_client


def tag_similarity_upadate() :
    print("해시태그 유사도 최신화 시작")
    tags = get_tags_count()
    tag_boards = create_tag_boards_dict(tags)
    price_score = analyze_price(tag_boards)
    title_score = analyze_title(tag_boards)
    score_list = price_score + title_score

    redis_client = get_redis_client()
    print(f"{len(tags)}개의 총 유사도 산출 시작 ...")
    # 총 유사도 점수
    for key_tag_id, value in score_list.items() :
        key = f"tag:similarity:{key_tag_id}"
        for tagId, sim_score in value.items() :
            redis_client.zadd(key, {tagId : sim_score})
    print(f"{len(tags)}개의 총 유사도 산출 완료 ...")

    # 가격 유사도 점수
    print(f"{len(tags)}개의 가격 유사도 저장 시작 ...")
    for key_tag_id, value in price_score.items() :
        key = f"tag:similarity:{key_tag_id}:price"
        for tagId, sim_score in value.items() :
            redis_client.hset(key, tagId, sim_score)
    print(f"{len(tags)}개의 가격 유사도 저장 완료 ...")

    # 제목 유사도 점수
    print(f"{len(tags)}개의 제목 유사도 산출 시작 ...")
    for key_tag_id, value in title_score.items() :
        key = f"tag:similarity:{key_tag_id}:title"
        for tagId, sim_score in value.items() :
            redis_client.hset(key, tagId, sim_score)
    print(f"{len(tags)}개의 제목 유사도 산출 완료 ...")

    print(f"{len(tags)}개의 해시태그 유사도 산출 완료 !!")


def create_tag_boards_dict(tagsId : list) :
    tag_boards = {}
    for t in tagsId:
        tag_boards[t] = get_board_by_tag(t)
    return tag_boards

def analyze_price(tag_boards : dict) :
    # 보드 ID가 Key, 가격이 value가 되는 딕셔너리 생성
    board_names = sorted({
        board.board_id
        for board_group in tag_boards.values()
        for board_list in board_group
        for board in board_list
    })

    # 각 벡터가 담길 리스트
    price_vect = []

    for tagId, boards in tag_boards.items() :
        # 벡터가 들어갈 딕셔너리를 0으로 초기화
        price_dict = {name: 0 for name in board_names}
        for board_group in boards:
            for board in board_group:
                price_dict[board.board_id] = board.price # 각 보드ID에 가격을 삽입
        #벡터를 price_vect에 삽입
        price_vect.append(price_dict)

    df = pd.DataFrame(price_vect, index=tag_boards.keys())

    cos_sim_matrix = cosine_similarity(df.values, df.values)
    cos_sim_df = pd.DataFrame(cos_sim_matrix, index=df.index, columns=df.index)
    return cos_sim_df


def analyze_title(tag_boards : dict) :

    title_tag_id = [k for k in tag_boards.keys()]
    title_vect = []
    for tagId, boards in tag_boards.items():
        s = ""
        for borad_group in boards :
            for board in borad_group:
                s += board.title
        title_vect.append(s)

    # TF-IDF로 벡터화
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(title_vect)

    # 코사인 유사도 분석
    cos_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    df = pd.DataFrame(cos_sim_matrix, index=title_tag_id, columns=title_tag_id)
    print(df)
    return df


