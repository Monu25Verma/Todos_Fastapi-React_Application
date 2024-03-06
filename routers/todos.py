import models
import uvicorn
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from typing import Annotated, Optional
from starlette import status
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
router = APIRouter(
    prefix="/todo",
    tags=['todos'],
    responses = {404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind = engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=300)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get("/test")
async def test(request : Request):
    return templates.TemplateResponse("edit-todo.html", {"request" : request})




@router.get("", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/get/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0, default=...)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='table not found')


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_id(user: user_dependency, db: db_dependency, todo_request: TodoRequest,
                         todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='table not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code= 401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="no data found")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
