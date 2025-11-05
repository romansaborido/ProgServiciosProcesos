
from fastapi import FastAPI
from routers import asignatura, profesor, auth_users
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.include_router(asignatura.router)
app.include_router(profesor.router)
app.include_router(auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")