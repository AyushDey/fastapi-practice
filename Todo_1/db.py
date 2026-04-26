from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from fastapi import Depends
from typing import Annotated

DB_URL = "sqlite:///./todosapp.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

class base(DeclarativeBase):
    pass


sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
