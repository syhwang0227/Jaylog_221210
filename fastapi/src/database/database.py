from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://root:!skfkzldna123@3.34.217.39:3306/jaylog"

# fastapi 공식문서 있는 코드
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# https://fastapi.tiangolo.com/ko/tutorial/sql-databases/
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DBase = declarative_base()