from fastapi import FastAPI,Request
from models import Base           #.Base is for testing file connection
from database import engine            #.Database is for testing file connection
from routers import auth, todos, admin, users, user_changepass, address
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse
import uvicorn

description = """
Book App API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    title="Todos App",
    description=description,
    summary="",
    version="0.0.1",
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
#app.include_router(address.router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)