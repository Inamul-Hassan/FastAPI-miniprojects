
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from passlib.hash import bcrypt


from models import User
from database import SessionLocal
from .auth import get_current_user

ALGORITHM = "HS256"
SECRET_KEY = "9baf8f01add42ea2f06e7f435cc5c9f9"

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


# install passlib and bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/me", status_code=200)
async def get_current_user(user: user_dependency, db: db_dependency):
    user_details = db.query(User).filter(
        User.id == user.get('user_id')).first()
    return user_details


@router.put("/change-password", status_code=200)
async def change_password(user: user_dependency, db: db_dependency, changepassword: ChangePassword):
    user_details = db.query(User).filter(
        User.id == user.get('user_id')).first()
    if bcrypt.verify(changepassword.old_password, user_details.hashed_password):
        user_details.hashed_password = bcrypt.hash(changepassword.new_password)
        db.commit()
        return {"message": "Password changed successfully"}
    else:
        return HTTPException(status_code=400, detail="Invalid password")
