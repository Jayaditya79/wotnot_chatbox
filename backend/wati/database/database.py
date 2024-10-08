
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Jayadityapgadmin$@localhost:7903/watnot'



# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Denmarks123$@localhost/wati_clone'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




