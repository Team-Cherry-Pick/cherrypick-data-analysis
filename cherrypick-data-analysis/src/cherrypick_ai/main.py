import asyncio
import uvicorn
from fastapi import FastAPI
from src.cherrypick_ai.config.env_config import DB_USERNAME
from src.cherrypick_ai.database import engine
from src.cherrypick_ai import models
from src.cherrypick_ai.services.hash_tag_similarity_updater import tag_similarity_upadate
from src.cherrypick_ai.services.user_interest_updater import updater_initialize, user_interest_updater_start
from src.cherrypick_ai.queries import hash_tag_query

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": DB_USERNAME}

# 테이블 생성 (기존 테이블이 있으면 무시)
models.Base.metadata.create_all(bind=engine)
# 컨슈머 그룹 생성, 가중치가 없다면 추가해줌
updater_initialize()


# 유저 관심사 실시간 분석 모듈 실행
asyncio.run(user_interest_updater_start())
# 해시태그 유사도 최신화 모듈 실행
tag_similarity_upadate()
# 웹서버 가동
uvicorn.run(app, host="localhost", port=8000)
