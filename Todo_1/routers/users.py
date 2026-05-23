from typing import Annotated
from db import db_dependency
from models import Users
from sqlalchemy import select, update
from sqlalchemy.orm import Session, defer
from fastapi import APIRouter, Depends, HTTPException
from request_models import CreateUserRequest, Token
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


