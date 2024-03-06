import uvicorn
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from models import Todos, Users
from pydantic import BaseModel, Field
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class verifypassword(BaseModel):
    password :\
        str
    new_password : str = Field(min_length = 6)

# class numberupdate(BaseModel):
#     phone_number: str
#     update_phonenumber : str = Field(gt = 0, lt = 11)


@router.get("", status_code=status.HTTP_200_OK)
async def all_info(user: user_dependency, db: db_dependency):
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Users).all()


@router.put("/change_pass", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, verify_password : verifypassword):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(verify_password.password, user_model.hashed_password):
        raise HTTPException(status_code = 401, detail = 'Error on password change')
    user_model.hashed_password = bcrypt_context.hash(verify_password.new_password)
    db.add(user_model)
    db.commit()

#uvicorn todosApp.main:app --reload


@router.put("/update_phoneNo/{phone_number}", status_code = status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db : db_dependency, phone_number : str):
    if user is None:
        raise HTTPException(status_code = 401, detail = "Authentication failed")
    print(user['id'])
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()