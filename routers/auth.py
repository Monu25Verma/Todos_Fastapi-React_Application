import sys
sys.path.append("..")

from starlette.responses import RedirectResponse
from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, , Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from starlette import status
from jose import jwt, JWTError

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
responses = {404: {"description": "Not found"}}
)


class LoginForm:
    def __init__(self, request:Request):
        self.request : Request = request
        self.username : Optional[str] = None
        self.password : Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

SECRET_KEY = "0fbac017273826e59e199f95f653c882244614d272a51d34affc2f278b6ba7b2"
ALGORITHM = "HS512"

templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
Oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



class createrequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number : str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request) #,token: Annotated[str, Depends(Oauth2_bearer)]):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id'),
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            logout(request)
            #return None
            #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user.')
        #users_details = {'username': username, 'id': user_id, 'user_role': user_role}
        # users_details['id'] = users_details['id'][0]
        # return users_details
        return {"username":username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.404, detail='Not Found')
        

@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency,
                create_user_request: createrequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number  = create_user_request.phone_number
    )
    user_model = db.query(Users).filter(Users.username == create_user_request.username)
    if user_model is None:
        raise HTTPException(status_code=401, detail='Username Already Taken!')
    db.add(create_user_model)
    db.commit()


@router.post("/token")#, response_model= Token)
async def login_for_access_token(response : Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta = token_expires)

    response.set_cookie(key = "access_token", value= token, httponly = True)
    #return {'access_token': token, 'token_type': 'bearer'}
    return True


@router.get("/", response_class= HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db : Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url = "/todo", status_code = status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response = response, form_data = form, db = db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("logout")
async def logout(request:Request):
    msg= "Logout Successfull"
    response = templates.TemplateResponse("home.html", {"request":request, "msg":msg})
    response.delete_cookie(key = "access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(request:Request):
    return templates.TemplateResponse("register.html", {"request":request})



@router.post("/register", response_class = HTMLRespons")
async def register_user(request:Request, email: str = Form(...), username : str = form(...),
                        first_name: str = Form(...), last_name : str = Form(...),
                        password: str = Form(...), password2 : str = Form(...),
                        db: Session = Depends(get_db)):
    
validation1 = db.query(models.Users).filter(models.Users.username == username).first()

validation2 = db.query(models.Users).filter(models.Users.email == email).first()

if password != password2 or validation1 is Not None or validation2 is not None:
    msg = "Invalid registration request"
    return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

user_model = models.Users()
user_model.username = username
user_model.email = username
user_model.first_name = first_name
user_model.last_name = last_name


hashed_password = get_password_hash(password)
user_model.hashed_password = hashed_password
user_model.is_active  =True

db.add(user_model)
db.commit()

msg = "User Created Successfully"
return templates.TemplateResponse("login.html",{"request": request, "msg": msg})




