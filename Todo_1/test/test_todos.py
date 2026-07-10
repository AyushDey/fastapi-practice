from sqlalchemy import create_engine

SQLite_DB_URL = 'sqlite://./test.db'
engine = create_engine(SQLite_DB_URL)

