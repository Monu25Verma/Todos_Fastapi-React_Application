import sys
sys.path.append("..")
import models
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from models import Todos, Users
from pydantic import BaseModel, Field
from database import SessionLocal, engine
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/users',
    tags=['users'],
responses = {404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind = engine)

templates = Jinja2Templates(directory = "templates")

def get_db():
    db = SessionLocal()
    try:
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
                        password: str = Form(...), password2 : str = Form(...),
                        db: Session = Depends(get_db)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url = "/auth", status_code = status.HTTP_302_FOUND)
    
  
    if user_data is None:
        if username == user_data.username and verifypassword(password, user_data.hashed_password):
            user_data.hashed_password = get_password_hash(password2)
            db.add(user_data)
            db.commit()

            msg = "Password updated Successfully"
    return templates.TemplateResponse("password_change.html", {"request":request, "user":user, "msg": msg})