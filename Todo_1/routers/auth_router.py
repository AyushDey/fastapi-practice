from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.get('/user')
async def get_user():
    return {"name": "foo"}