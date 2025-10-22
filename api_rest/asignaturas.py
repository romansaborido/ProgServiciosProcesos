
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Asignatura(BaseModel):
    id: int
    titulo: str
    num_horas: int
    id_profesor: int

asignaturas_list = [
    Asignatura(id=1, titulo="Matemáticas", num_horas=40, id_profesor=1),
    Asignatura(id=2, titulo="Física", num_horas=35, id_profesor=2),
    Asignatura(id=3, titulo="Química", num_horas=30, id_profesor=3),
    Asignatura(id=4, titulo="Historia", num_horas=25, id_profesor=4),
    Asignatura(id=5, titulo="Lengua", num_horas=28, id_profesor=5),
]



@app.get("/asignaturas")
def get_asignaturas():
    return asignaturas_list

@app.get("/asignaturas/{id_asignatura}")
def get_asignatura_id(id_asignatura: int):
    for asignatura in asignaturas_list:
        if asignatura.id == id_asignatura:
            return asignatura
    raise HTTPException(status_code=404, detail="Asignatura no encontrada")


@app.post("/asignaturas",status_code=201)
def add_asignatura(asignatura: Asignatura):
    asignatura.id = nextId()
    asignaturas_list.append(asignatura)
    return asignatura


@app.delete("/asignaturas/{id_asignatura}")
def delete_asignatura(id_asignatura: int):
    for asignatura_saved in asignaturas_list:
        if asignatura_saved.id == id_asignatura:
            asignaturas_list.remove(asignatura_saved)
            return {}
    raise HTTPException(status_code=404, detail="Asignatura no encontrada")


@app.put("/asignaturas/{id_asignatura}")
def modify_asignatura(id_asignatura: int, asignatura: Asignatura):
    for index, saved_asignatura in enumerate(asignaturas_list):
        if saved_asignatura.id == id_asignatura:
            asignatura.id = id_asignatura
            asignaturas_list[index] = asignatura
            return asignatura
    raise HTTPException(status_code=404, detail="Asignatura no encontrada")







def nextId():
    return (max(asignaturas_list, key=lambda asignatura: asignatura.id).id + 1)