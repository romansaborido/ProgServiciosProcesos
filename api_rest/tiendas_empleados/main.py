
from fastapi import FastAPI
from routers import empleado, tienda
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.include_router(empleado.router)
app.include_router(tienda.router)
app.mount("/static", StaticFiles(directory="static"), name="static")