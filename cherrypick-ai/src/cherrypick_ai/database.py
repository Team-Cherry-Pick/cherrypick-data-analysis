from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 연결 정보
DATABASE_URL = "mysql+pymysql://root:password@serverprac.cj6koc6yqngh.ap-northeast-2.rds.amazonaws.com/serverprac"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 정의를 위한 Base 클래스
Base = declarative_base()
