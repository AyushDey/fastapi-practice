from typing import Annotated

import models
from db import db_dependency
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from request_models import TodoRequest
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from starlette import status
from .auth_router import get_current_user

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

#Create the db
#models.base.metadata.create_all(bind=engine)

user_dependency = Annotated[dict, Depends(get_current_user)]

def check_admin(user: user_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorised')
    return True

@admin_router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    # if user is None or user.get('user_role') != 'admin':
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
    if check_admin(user):
        stmt = select(Todos)
        return db.scalars(stmt).all()

@admin_router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todos(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if check_admin(user):
        stmt = delete(Todos).where(Todos.id == todo_id)
        result = db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Todo details found')
        # db.delete(todo_data)
        db.commit()