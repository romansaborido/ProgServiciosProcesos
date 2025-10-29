
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/tiendas", tags=["tiendas"])


class Tienda(BaseModel):
    id: int
    domicilio: str
    telefono: int
    precio_alquiler: float


tiendas_list = [
    Tienda(id=1, domicilio="Calle Mayor 123", telefono=600123456, precio_alquiler=1200.50),
    Tienda(id=2, domicilio="Avenida Central 45", telefono=600234567, precio_alquiler=1500.00),
    Tienda(id=3, domicilio="Plaza Sol 8", telefono=600345678, precio_alquiler=900.75),
    Tienda(id=4, domicilio="Calle Luna 77", telefono=600456789, precio_alquiler=2000.20),
    Tienda(id=5, domicilio="Avenida Estrella 9", telefono=600567890, precio_alquiler=1750.00)
]


@router.get("/")
def get_tiendas():
    return tiendas_list


@router.get("/{id_tienda}")
def get_tienda(id_tienda: int):
    tienda = [tienda for tienda in tiendas_list if tienda.id == id_tienda]
    if tienda:
        return tienda
    else:
        return "Error : Tienda no encontrada"


@router.get("/query/")
def get_tienda_query(id: int):
    tienda = [tienda for tienda in tiendas_list if tienda.id == id]
    if tienda:
        return tienda
    else:
        return "Error : Tienda no encontrada"


@router.post("/", status_code=201, response_model=Tienda)
def add_tienda(tienda: Tienda):
    tienda.id = nextId()
    tiendas_list.append(tienda)
    return tienda


@router.put("/{id_tienda}", response_model=Tienda)
def modify_tienda(id_tienda: int, tienda: Tienda):
    for index, saved_tienda in enumerate(tiendas_list):
        if saved_tienda.id == id_tienda:
            tienda.id == id_tienda
            tiendas_list[index] = tienda
            return tienda
    raise HTTPException(status_code=404, detail="Tienda no encontrada")


@router.delete("/{id_tienda}")
def delete_tienda(id_tienda: int):
    for saved_tienda in tiendas_list:
        if saved_tienda.id == id_tienda:
            tiendas_list.remove(saved_tienda)
            return {}
    raise HTTPException(status_code=404, detail="Tienda no encontrada")



def nextId():
    return (max(tiendas_list, key=lambda t: t.id).id+1)
