
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/empleados", tags=["empleados"])


class Empleado(BaseModel):
    id: int
    nombre: str
    apellidos: str
    telefono: int
    correo: str
    num_cuenta: str
    id_tienda: int


empleados_list = [
    Empleado(id=1, nombre="Carlos", apellidos="Gómez", telefono=600111222, correo="carlos.gomez@email.com", num_cuenta="ES7620770024003102575766", id_tienda=1),
    Empleado(id=2, nombre="Lucía", apellidos="Martínez", telefono=600222333, correo="lucia.martinez@email.com", num_cuenta="ES4421000418450200051332", id_tienda=2),
    Empleado(id=3, nombre="Miguel", apellidos="Sánchez", telefono=600333444, correo="miguel.sanchez@email.com", num_cuenta="ES9121000418450200051345", id_tienda=3),
    Empleado(id=4, nombre="Ana", apellidos="López", telefono=600444555, correo="ana.lopez@email.com", num_cuenta="ES7921000418450200051367", id_tienda=4),
    Empleado(id=5, nombre="Javier", apellidos="Ramírez", telefono=600555666, correo="javier.ramirez@email.com", num_cuenta="ES3021000418450200051389", id_tienda=5)
]



@router.get("/")
def get_empleados():
    return empleados_list


@router.get("/{id_empleado}")
def get_empleado(id_empleado: int):
    empleado = [empleado for empleado in empleados_list if empleado.id == id_empleado]
    if empleado:
        return empleado
    else:
        return "Error : Empleado no encontrado"


@router.get("/query/")
def get_empleado_query(id: int):
    empleado = [empleado for empleado in empleados_list if empleado.id == id]
    if empleado:
        return empleado
    else:
        return "Error : Empleado no encontrado"


@router.delete("/{id_empleado}")
def delete_empleado(id_empleado: int):
    for saved_empleado in empleados_list:
        if saved_empleado.id == id_empleado:
            empleados_list.remove(saved_empleado)
            return {}
    raise HTTPException(status_code=404, detail="Empleado no encontrado")


@router.put("/{id_empleado}", response_model=Empleado)
def modify_empleado(id_empleado: int, empleado: Empleado):
    for index, saved_empleado in enumerate(empleados_list):
        if saved_empleado.id == id_empleado:
            empleado.id = id_empleado
            empleados_list[index] = empleado
            return empleado
    raise HTTPException(status_code=404, detail="Empleado no encontrado")


@router.post("/", status_code=201, response_model=Empleado)
def add_empleado(empleado: Empleado):
    empleado.id = nextId()
    empleados_list.append(empleado)
    return empleado


def nextId():
    return (max(empleados_list, key=lambda e: e.id).id+1)