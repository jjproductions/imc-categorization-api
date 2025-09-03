from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings
from dotenv import load_dotenv

load_dotenv()

DB_PW = os.getenv("db_iom_password")
DB_USER = os.getenv("db_iom_user")

# write to console the values of settings
print(settings.DB_SERVER)
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{DB_USER}:{DB_PW}@{settings.DB_SERVER}/{settings.DB_IOM_DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
