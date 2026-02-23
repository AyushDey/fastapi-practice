from typing import Annotated
from db import sessionlocal
from models import Users
from sqlalchemy.orm import Session
from sqlalchemy import insert
from fastapi import APIRouter, Depends
from request_models import CreateUserRequest
from starlette import status
from passlib.context import CryptContext

auth_router = APIRouter()

crypt_context = CryptContext(
    schemes=["argon2"],
    argon2__type="ID",
    argon2__memory_cost=19456,
    argon2__time_cost=2,
    argon2__parallelism=2,
    deprecated="auto",
)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@auth_router.post('/auth', status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserRequest, db: db_dependency):
    # `hash_password` already truncates to 72 bytes, so we can rely on it
    create_user_model = Users(
        username=user_request.username,
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=crypt_context.hash(user_request.password),
        is_active=True,
        role=user_request.role
    )
    db.add(create_user_model)
    db.commit()
    
