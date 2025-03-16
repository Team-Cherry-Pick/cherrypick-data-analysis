from fastapi import FastAPI
from src.cherrypick_ai.config import DB_USERNAME
from src.cherrypick_ai.database import Base, engine
from src.cherrypick_ai import models

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": DB_USERNAME}

# 테이블 생성 (기존 테이블이 있으면 무시)
models.Base.metadata.create_all(bind=engine)