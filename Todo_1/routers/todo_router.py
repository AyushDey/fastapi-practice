from typing import Annotated

import models
from db import engine, sessionlocal
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from request_models import TodoRequest
from sqlalchemy import insert
from sqlalchemy.orm import Session
from starlette import status

todo_router = APIRouter()


# Connect to DB
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


# Creating dependency injection for db
db_dependency = Annotated[Session, Depends(get_db)]


@todo_router.get("/todos/", status_code=status.HTTP_200_OK)
async def get_all_data(db: db_dependency):
    rows = db.query(Todos).all()
    return rows


@todo_router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(ge=1)):
    record = db.query(Todos).filter_by(id=todo_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="No records found with {todo_id}")
    else:
        return record


@todo_router.post("/todos/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, request: TodoRequest):
    todo_data = Todos(**request.model_dump())
    if todo_data is None:
        raise HTTPException(status_code=404, detail="No Todo inserted")
    else:
        db.add(todo_data)
        db.commit()


@todo_router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, request: TodoRequest, todo_id: int = Path(ge=1)
):
    todo_data = db.query(Todos).filter_by(id=todo_id).first()
    if todo_data is None:
        raise HTTPException(status_code=404, detail="No todos found")
    else:
        response_todo = Todos(**request.model_dump())
        todo_data.title = response_todo.title
        todo_data.description = response_todo.description
        todo_data.priority = response_todo.priority
        todo_data.complete = response_todo.complete
        db.add(todo_data)
        db.commit()


@todo_router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db: db_dependency, todo_id: int = Path(ge=1)):
    todo_data = db.query(Todos).filter_by(id=todo_id).first()
    if todo_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No todo found"
        )
    else:
        db.delete(todo_data)
        db.commit()
