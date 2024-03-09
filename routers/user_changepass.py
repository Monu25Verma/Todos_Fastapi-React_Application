import sys

from pipenv.patched.pip._internal.network.session import user_agent
from sqlalchemy.sql.functions import user

import models
sys.path.append("..")
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import SessionLocal, engine
from .auth import get_current_user, get_password_hash
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
from models import Users
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags=['users'],
responses = {404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind = engine)

templates = Jinja2Templates(directory = "templates")
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    user_name : str
    password : str
    new_password : str


@router.get("/edit_password", response_class=HTMLResponse)
async def edit_password(request:Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url = "/auth", status_code = status.HTTP_302_FOUND)

    return templates.TemplateResponse("password_change.html", {"request":request, "user":user})


@router.post("/edit_password", response_class=HTMLResponse)
async def register_user(request:Request, username : str = Form(...),
                        original_password: str = Form(...), change_password : str = Form(...),
                        db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url = "/auth", status_code = status.HTTP_302_FOUND)
    user_db = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_db is not None:
        if username == user_db.username and bcrypt_context.verify(original_password, user_db.hashed_password):
            user_db.hashed_password = get_password_hash(change_password)
            db.add(user_db)
            db.commit()
            msg = "Password updated Successfully"
            return templates.TemplateResponse("login.html",{"request": request, "msg": msg})
    else:
        msg = "User not present in DB!"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})