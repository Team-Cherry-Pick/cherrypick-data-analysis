import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
PROFILE = os.getenv('PROFILE')

DB_URL = os.getenv("DB_URL")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

REDIS_URL = os.getenv("REDIS_URL")
REDIS_PORT = os.getenv("REDIS_PORT")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")
SLACK_URL = os.getenv("SLACK_URL")

DEV_POST_DEAL_URL = os.getenv("DEV_POST_DEAL_URL")
DEV_REPIK_TOKEN = os.getenv("DEV_REPIK_TOKEN")
PROD_POST_DEAL_URL = os.getenv("PROD_POST_DEAL_URL")
PROD_REPIK_TOKEN = os.getenv("PROD_REPIK_TOKEN")
DEAL_INFO_URL = os.getenv("DEAL_INFO_URL")

