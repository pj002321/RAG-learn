"""
데이터베이스 연결을 담당합니다. 이 파일이 가진 것은 네 가지뿐입니다.

engine        실제 DB 와 연결하는 통로
SessionLocal  DB 작업 한 번에 쓰는 세션을 만들어 주는 공장
Base          모든 테이블 모델이 물려받는 기준
get_db        요청 하나마다 세션을 열고 닫아 주는 함수
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

# SQLite 는 여러 스레드에서 접근할 때 이 옵션이 필요합니다. PostgreSQL 은 필요 없습니다.
# 이렇게 해두면 Supabase 로 옮길 때 이 파일은 고치지 않아도 됩니다.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()