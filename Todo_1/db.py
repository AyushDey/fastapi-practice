from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_URL = "sqlite:///./todosapp.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

class base(DeclarativeBase):
    pass


sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
