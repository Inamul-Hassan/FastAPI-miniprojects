from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from passlib.hash import bcrypt

from models import User
from database import SessionLocal


router = APIRouter()

# install passlib and bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class UserRequest(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    role: str


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return "User Not Found"
    if not bcrypt.verify(password, user.hashed_password):
        return "Wrong Password"
    return user


@router.get("/auth")
async def get_users(db: db_dependency):
    all_users = db.query(User).all()
    return all_users


@router.post("/auth/create_user")
async def create_user(db: db_dependency, user: UserRequest):
    create_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return user


@router.post("/auth/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if isinstance(user, str):
        return {"Error": user}
    return f"{form_data.username} Authenticated!"
