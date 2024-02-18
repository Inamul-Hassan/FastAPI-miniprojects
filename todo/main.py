from fastapi import FastAPI

# import models

from database import engine, Base
from routers import auth, todos

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

Base.metadata.create_all(bind=engine)
