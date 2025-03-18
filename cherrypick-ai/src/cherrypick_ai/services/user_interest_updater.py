import redis
import redis.exceptions
from src.cherrypick_ai.config.redis_config import get_redis_client
from src.cherrypick_ai.services.method import method

STREAM_NAME = "USER_BEHAVIOR_STREAM"
CONSUMER_GROUP = "REALTIME_USER_INTEREST_UPDATERS"
CONSUMER_NAME = "REALTIME_USER_INTEREST_UPDATER"

def create_group() :

    # 컨슈머 그룹 생성 (존재하지 않으면 생성)
    try:

        client = get_redis_client()
        print(method.PURCHASE.name)

        if not client.exists(method.PURCHASE.name) :
            client.set(method.PURCHASE.name, method.PURCHASE.value)
        if not client.exists(method.VIEW.name) :
            client.set(method.VIEW.name, method.VIEW.value)
        if not client.exists(method.RECOMMEND.name) :
            client.set(method.RECOMMEND.name, method.RECOMMEND.value)


        client.xgroup_create(STREAM_NAME, CONSUMER_GROUP, id=0, mkstream=True)
        print(f"✅ 컨슈머 그룹 '{CONSUMER_GROUP}' 생성 완료")

    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"⚠️ 컨슈머 그룹 '{CONSUMER_GROUP}' 이미 존재")
        else:
            raise e



# 비동기 Redis 스트림 리스너 함수
async def user_interest_updater_start():
    # Redis 비동기 클라이언트 설정
    client = get_redis_client()

    # 스트림에서 새로운 메시지를 감지
    print(f"Listening to stream: {STREAM_NAME}...\n")
    while True:
        # XREAD 명령어로 실시간 스트림 읽기 (블로킹 모드)
        response = response = client.xreadgroup(
            groupname=CONSUMER_GROUP,
            consumername=CONSUMER_NAME,
            streams={STREAM_NAME: ">"},  # ">" = 새로운 메시지만 읽음
            count=1,
            block=5000  # 5초 동안 블로킹 (없으면 즉시 종료)
        )

        # 각 스트림 메시지 처리
        for stream, messages in response:
            for message_id, fields in messages:
                print(f"New message received: ID={message_id}")
                user_interest_update(fields)
                print("-" * 40)


def user_interest_update(fields : dict):
    print(fields.get("method"))



