from fastapi import FastAPI
from routers import auth_router, todo_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)
