
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/profesores", tags=["profesores"])



# Entidad Profesor
class Profesor(BaseModel):
    id: int
    dni: str
    nombre: str
    apellidos: str
    telefono: str
    direccion: str
    cuentaBancaria: str


# Lista de profesores (datos de ejemplo)
profesores_list = [
    Profesor(id=1, dni="12345678A", nombre="Laura", apellidos="García López",
             telefono="+34 600 111 222", direccion="Calle Mayor 10, Madrid",
             cuentaBancaria="ES12 3456 7890 1234 5678 9012"),
    Profesor(id=2, dni="23456789B", nombre="Carlos", apellidos="Martínez Pérez",
             telefono="+34 600 333 444", direccion="Avenida Sol 25, Barcelona",
             cuentaBancaria="ES98 7654 3210 9876 5432 1098"),
    Profesor(id=3, dni="34567890C", nombre="Ana", apellidos="Fernández Ruiz",
             telefono="+34 600 555 666", direccion="Plaza del Carmen 8, Valencia",
             cuentaBancaria="ES45 6789 0123 4567 8901 2345"),
]



# Obtener todos los profesores
@router.get("/")
def get_profesores():
    return profesores_list



# Buscar profesor por ID
@router.get("/{id_profesor}")
def get_profesor(id_profesor: int):
    profesores = [p for p in profesores_list if p.id == id_profesor]
    if len(profesores) != 0:
        return profesores[0]
    else:
        return {"error": "Profesor no encontrado"}


# Buscar profesor por DNI
@router.get("/dni/{dni_profesor}")
def get_profesor_by_dni(dni_profesor: str):
    profesores = [p for p in profesores_list if p.dni.lower() == dni_profesor.lower()]
    if len(profesores) != 0:
        return profesores[0]
    else:
        return {"error": "Profesor no encontrado"}



# Eliminar profesor por ID
@router.delete("/{id_profesor}")
def delete_profesor_by_id(id_profesor: int):
    for saved_profesor in profesores_list:
        if saved_profesor.id == id_profesor:
            profesores_list.remove(saved_profesor)
            return {}
    raise HTTPException(status_code=404, detail="Profesor no encontrado")


# Eliminar profesor por DNI
@router.delete("/dni/{dni_profesor}")
def delete_profesor_by_dni(dni_profesor: str):
    for saved_profesor in profesores_list:
        if saved_profesor.dni == dni_profesor:
            profesores_list.remove(saved_profesor)
            return {}
    raise HTTPException(status_code="404", details="Profesor no encontrado")



# Modificar profesor por ID
@router.put("/{id_profesor}", response_model=Profesor)
def modify_profesor_by_id(profesor: Profesor, id_profesor: int):
    for index, saved_profesor in enumerate(profesores_list):
        if saved_profesor.id == id_profesor:
            profesor.id = id_profesor
            profesores_list[index] = profesor
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")


# Modificar profesor por DNI
@router.put("/dni/{dni_profesor}", response_model=Profesor)
def modify_profesor_by_dni(profesor: Profesor, dni_profesor: str):
    for index, saved_profesor in enumerate(profesores_list):
        if saved_profesor.dni == dni_profesor:
            profesor.dni = dni_profesor
            profesores_list[index] = profesor
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")



# Añadir profesor
@router.post("/", status_code=201, response_model=Profesor)
def add_profesor(profesor: Profesor):
    profesor.id = nextId()
    profesores_list.append(profesor)
    return profesor


def nextId():
    return max(profesores_list, key=lambda p: p.id).id + 1
