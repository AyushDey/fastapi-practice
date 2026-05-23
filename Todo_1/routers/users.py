from typing import Annotated
from db import db_dependency
from models import Users
from sqlalchemy import select, update
from sqlalchemy.orm import Session, defer
from fastapi import APIRouter, Depends, HTTPException
from request_models import CreateUserRequest, Token, ChangePassword, UserResponse
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

@user_router.get('/', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    if check_user(user):
        stmt = select(Users).where(Users.id == user.get('id'))
        user_details = db.scalar(stmt)
        return user_details

@user_router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(user: user_dependency, db: db_dependency, password_request: ChangePassword):
    if check_user(user):
        stmt = select(Users).where(Users.id == user.get('id'))
        user_info = db.scalar(stmt)
        if not crypt_context.verify(password_request.old_password, user_info.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong old password')
        
        if password_request.new_password != password_request.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='New password and confirm password does not match')
        
        new_password = crypt_context.hash(password_request.new_password)
        stmt = update(Users).where(Users.id == user.get('id')).values(hashed_password = new_password)
        db.execute(stmt)
        db.commit()    
