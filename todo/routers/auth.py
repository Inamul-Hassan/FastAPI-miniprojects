from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from passlib.hash import bcrypt
from jose import JWTError, jwt

from models import User
from database import SessionLocal

ALGORITHM = "HS256"
SECRET_KEY = "9baf8f01add42ea2f06e7f435cc5c9f9"

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# install passlib and bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


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


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(db: Session, username: str, password: str) -> User | str:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return "User Not Found"
    if not bcrypt.verify(password, user.hashed_password):
        return "Wrong Password"
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    expires = datetime.utcnow() + expires_delta
    to_encode = {"sub": username, "user_id": user_id, "exp": expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        token_data = {"username": username, "user_id": user_id}
    except JWTError:
        raise credentials_exception
    return token_data


@router.get("/get_users")
async def get_users(db: db_dependency):
    all_users = db.query(User).all()
    return all_users


@router.post("/create_user")
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


@router.post("/token", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if isinstance(user, str):
        return HTTPException(
            status_code=401,
            detail=user)
    token = {
        "access_token": create_access_token(user.username, user.id, timedelta(minutes=20)),
        "token_type": "bearer"
    }
    return token
