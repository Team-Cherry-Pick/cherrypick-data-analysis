from fastapi import FastAPI
from src.cherrypick_ai.config import DB_USERNAME
from src.cherrypick_ai.database import engine

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": DB_USERNAME}

# ✅ 애플리케이션 시작 시 DB 연결 확인
@app.on_event("startup")
def startup_event():
    try:

        with engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(text("SELECT 1"))
            print("✅ 데이터베이스 연결 성공!")
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")