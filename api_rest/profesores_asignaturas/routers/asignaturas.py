from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.client import db_client

router = APIRouter(prefix="/asignaturas", tags=["asignaturas"])


# Entidad asignatura
class Asignatura(BaseModel):
    id: int
    titulo: str
    num_horas: int
    id_profesor: int

asignaturas_list = [
    Asignatura(id=1, titulo="Matemáticas", num_horas=60, id_profesor=1),
    Asignatura(id=2, titulo="Historia", num_horas=45, id_profesor=2),
    Asignatura(id=3, titulo="Programación", num_horas=80, id_profesor=3)
]



# Obtener todas las asignaturas
@router.get("/")
def get_asignaturas():
    return db_client


# Obtener asignatura por ID
@router.get("/{id}")
def get_asignatura_by_id(id: int):
    asignatura = [asignatura for asignatura in asignaturas_list if asignatura.id == id]
    if asignatura:
        return asignatura
    else:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada")
    

# Obtener asignatura con query
@router.get("")
def get_asignatura_query(id : int):
    asignatura = [asignatura for asignatura in asignaturas_list if asignatura.id == id]
    if asignatura:
        return asignatura
    raise HTTPException(status_code=404, detail="No asignatura found")




# Añadir asignatura
@router.post("/", status_code=201, response_model=Asignatura)
def add_asignatura(asignatura: Asignatura):
    asignatura.id = nextId()
    db_client.append(asignatura)
    return asignatura



# Modificar asignatura por ID
@router.put("/{id}", response_model=Asignatura)
def modify_asignatura(id: int, asignatura: Asignatura):
    for index, saved_asignatura in enumerate(asignaturas_list):
        if saved_asignatura.id == id:
            asignatura.id = id
            asignaturas_list[index] = asignatura
            return asignatura
    raise HTTPException(status_code=404, detail="Error : Asignatura no encontrada")



# Eliminar asignatura por ID
@router.delete("/{id}")
def delete_asignatura(id: int):
    for saved_asignatura in asignaturas_list:
        if saved_asignatura.id == id:
            asignaturas_list.remove(saved_asignatura)
            return {}
    raise HTTPException(status_code=404, detail="Error : Asignatura no encontrada")



def nextId():
    return (max(asignaturas_list, key=lambda p: p.id).id+1)