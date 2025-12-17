from fastapi import FastAPI
from routers import colegios, alumnos, auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(colegios.router)
app.include_router(alumnos.router)
app.include_router(auth_users.router)