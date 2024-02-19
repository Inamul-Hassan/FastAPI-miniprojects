from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

# import models
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=25)
    description: str = Field(max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# We can directly define them inside the finction parameter but this is a to make the code reusable since we will be doing the same thing in other requests
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_data = db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get('user_id')).first()
    if todo_data is not None:
        return todo_data
    else:
        return HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def post_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        return HTTPException(status_code=401, detail="Unauthorized")

    todo_data = Todos(**todo_request.model_dump(),
                      owner_id=user.get("user_id"))

    db.add(todo_data)
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    # request_data = Todo(**todo_request.model_dump())

    todo_data = db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get('user_id')).first()
    if todo_data is None:
        return HTTPException(status_code=404, detail="Todo not found")

    todo_data.title = todo_request.title
    todo_data.description = todo_request.description
    todo_data.priority = todo_request.priority
    todo_data.completed = todo_request.completed

    db.add(todo_data)
    db.commit()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo_data = db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get('user_id')).first()
    if todo_data is None:
        return HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_data)
    db.commit()
