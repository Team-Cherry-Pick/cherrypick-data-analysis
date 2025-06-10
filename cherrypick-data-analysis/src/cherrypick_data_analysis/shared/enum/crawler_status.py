import enum

class Status(enum.Enum):
    RUNNING = "RUNNING"     # 작동 중, 크롤링 중
    STOPPED = "STOPPED"     # 인위적으로 멈춘 정지 상태
    WAITING = "WAITING"     # 다음 글이 올라오길 대기 중
    BREAK = "BREAK"         # 완전 중지

class DataKey(enum.Enum):
    TOTAL_COUNT = "TOTAL_COUNT"
    FAILURE_COUNT = "FAILURE_COUNT"
    QUEUED_COUNT = "QUEUED_COUNT"
    NOW_CRAWLING = "NOW_CRAWLING"
    START_TIME = "START_TIME"
    AVERAGE_DURATION = "AVERAGE_DURATION"
    LAST_SAVED_TIME = "LAST_SAVED_TIME"
    DELAY_TIME = "DELAY_TIME"



