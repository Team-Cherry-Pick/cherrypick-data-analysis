import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from cherrypick_data_analysis.shared.config.env import DB_URL, DB_USERNAME, DB_PASSWORD


# MySQL 연결 정보`
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)#, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 세션 반환 함수
def get_session()->Session:
    return SessionLocal()

logging.basicConfig(level=logging.INFO)

# 모델 정의를 위한 Base 클래스
Base = declarative_base()

