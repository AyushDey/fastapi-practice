from typing import Annotated
from db import db_dependency
from models import Users
from sqlalchemy import select, update
from sqlalchemy.orm import Session, defer
from fastapi import APIRouter, Depends, HTTPException
from request_models import CreateUserRequest, Token, ChangePassword
from starlette import status
from .auth_router import crypt_context, user_dependency

user_router = APIRouter(
    prefix= '/user',
    tags=['user']
)

def check_user(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorised')
    return True

@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    if check_user(user):
        stmt = select(Users).where(Users.id == user.get('id')).options(defer(Users.hashed_password)) # Defere doesn't delete it from the ORM object it just makes sure it doesn't appear in print
        user_details = db.scalars(stmt).first()
        return user_details

@user_router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(user: user_dependency, db: db_dependency, password_request: ChangePassword):
    if check_user(user):
        stmt = select(Users).where(Users.id == user.get('id'))
        user_info = db.scalars(stmt).first()
        if not crypt_context.verify(password_request.old_password, user_info.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong old password')
        
        if password_request.new_password == password_request.confirm_password:
            new_password = crypt_context.hash(password_request.new_password)
            stmt = update(Users).where(Users.id == user.get('id')).values(hashed_password = new_password)
            db.execute(stmt)
            db.commit()

