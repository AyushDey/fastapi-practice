from db import base
from sqlalchemy import Boolean, Column, Integer, String


class Todos(base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
