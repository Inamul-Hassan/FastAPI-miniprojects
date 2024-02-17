from fastapi import FastAPI

# import models
from models import Base
from database import engine
from routers import auth, todos

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)

Base.metadata.create_all(bind=engine)
