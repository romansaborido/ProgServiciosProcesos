
from fastapi import FastAPI
from routers import auth_users, asignaturas, profesores, asignaturas_bd, profesores_bd
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.include_router(asignaturas.router)
app.include_router(profesores.router)
app.include_router(auth_users.router)
app.include_router(asignaturas_bd.router)
app.include_router(profesores_bd.router)
app.mount("/static", StaticFiles(directory="static"), name="static")