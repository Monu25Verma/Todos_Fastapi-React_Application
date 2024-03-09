from fastapi import FastAPI,Request
from models import Base           #.Base is for testing file connection
from database import engine            #.Database is for testing file connection
from routers import auth, todos, admin, users, user_changepass
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

description = """
Book App API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    title="Book App",
    description=description,
    summary="",
    version="0.0.2",
    contact={
        "Made By": "Monu Verma",
        "url": "https://github.com/Monu25Verma"
    },
    license_info={
        "name": "FASTAPI 1.0"
    }
)

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory = "static"), name = "static")


@app.get('/healthy', tags=["Service Check"])
def health_check():
    return {'status' : 'Healthy'}


@app.get("/")
async def RedirectResponse(url = "/todo/", status_code = status.HTTP_302_FOUND):
    return


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(user_changepass.router)


