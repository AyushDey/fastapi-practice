import models
from db import db_dependency
from fastapi import APIRouter, HTTPException, Path
from models import Todos
from request_models import TodoRequest
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from .auth_router import user_dependency

todo_router = APIRouter(
    prefix='/todos',
    tags=['todo']
)

#Create the db
#models.base.metadata.create_all(bind=engine)

@todo_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_data(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    stmt = select(Todos).where(Todos.owner_id == user.get('id'))
    rows = db.scalars(stmt).all()
    return rows


@todo_router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    
    stmt = select(Todos).where(Todos.id==todo_id and Todos.owner_id == user.get('id'))
    record = db.scalars(stmt).first()
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No records found with {todo_id}")
    else:
        return record


@todo_router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    
    todo_data = Todos(**request.model_dump(), owner_id=user.get('id'))
    if todo_data is None:
        raise HTTPException(status_code=404, detail="No Todo inserted")
    else:
        db.add(todo_data)
        db.commit()


@todo_router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency, db: db_dependency, request: TodoRequest, todo_id: int = Path(ge=1)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    
    todo_stmt = select(Todos).where(Todos.id == todo_id and Todos.owner_id == user.get('id'))
    todo_data = db.scalars(todo_stmt).first()
    if todo_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No todos found")
    else:
        todo_data.title = request.title
        todo_data.description = request.description
        todo_data.priority = request.priority
        todo_data.complete = request.complete
        db.add(todo_data)
        db.commit()


@todo_router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    
    todo_stmt = select(Todos).where(Todos.id==todo_id, Todos.owner_id == user.get('id'))
    todo_data = db.scalars(todo_stmt).first()
    if todo_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No todo found"
        )
    else:
        db.delete(todo_data)
        db.commit()
