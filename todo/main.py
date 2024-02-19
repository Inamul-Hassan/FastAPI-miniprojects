from fastapi import FastAPI

# import models

from database import engine, Base
from routers import auth, todos, user

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)
