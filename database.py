import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env 환경 변수에서 DB 접속 정보를 가져옵니다.
user = os.getenv("POSTGRES_USER", "myuser")
password = os.getenv("POSTGRES_PASSWORD", "mypassword")
db_name = os.getenv("POSTGRES_DB", "tododb")

# 도커 네트워크 안에서 DB 컨테이너 호스트 이름은 'db'가 됩니다.
DATABASE_URL = f"postgresql://{user}:{password}@db:5432/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()