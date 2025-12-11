
from fastapi import FastAPI
from routers.bd import Empleados, Tiendas   
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.include_router(Empleados.router)
app.include_router(Tiendas.router)