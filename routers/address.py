import models
import uvicorn
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
#from typing import Annotated, Optional
from starlette import status
from starlette.responses import  RedirectResponse
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from database import engine, SessionLocal

router  = APIRouter(
    prefix = ["/address"],
    tags = ["/address"],
    responses= {404: {'Description':"data not Found"}}
    
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address1 : str
    address2 : str
    city : str
    state : str
    country: str
    postalcode : str
    apt_num : Optional[str]


# @router.post("/")
# async def Create_address(address: Address, user: dict= Depends(get_current_user),
#                         db:Session= Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     address_model = models.Address()
#     address_model.address1 = address.address1
#     address_models.address2 = address.address2
#     address_model.city = address.city
#     address_model.state = address.state
#     address_model.country = address.country
#     address_model.postalcode = address.postalcode
      address_model.apt_num = address.apt_num

#     db.add(address_model)
#     db.flush()

#     user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
#     user_model.address_id = address_model.id

#     db.add(user_model)
#     db.commit()






