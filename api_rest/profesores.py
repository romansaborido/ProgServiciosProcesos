from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()



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
@app.get("/profesores")
def get_profesores():
    return profesores_list


# Buscar profesor por ID
@app.get("/profesores/{id_profesor}")
def get_profesor(id_profesor: int):
    profesores = [p for p in profesores_list if p.id == id_profesor]
    if profesores:
        return profesores[0]
    else:
        return {"error": "Profesor no encontrado"}


# Buscar profesor por DNI
@app.get("/profesores/dni/{dni_profesor}")
def get_profesor_by_dni(dni_profesor: str):
    profesores = [p for p in profesores_list if p.dni.lower() == dni_profesor.lower()]
    if profesores:
        return profesores[0]
    else:
        return {"error": "Profesor no encontrado"}


# Añadir un profesor
@app.post("/profesores", status_code=201)
def add_profesor(profesor:Profesor):
    profesor.id = nextId()
    profesores_list.append(profesor)
    return profesor


# Eliminar un profesor
@app.delete("/profesores/{id}")
def remove_profesor(id: int):
    for profesor in profesores_list:
        if profesor.id == id:
            profesores_list.remove(profesor)
            return {}
    raise HTTPException(status_code=401, detail="Profesor no encontrado")


# Modificar un profesor
@app.put("/profesores/{id}")
def modify_profesor(id: int, profesor: Profesor):
    for index, saved_profesor in enumerate(profesores_list):
        if saved_profesor.id == id:
            profesor.id = id
            profesores_list[index] = profesor
            return profesor
    raise HTTPException(status_code=401, detail="Profesor no encontrado")



# Funcion para obtener el proximo id
def nextId():
    return (max(profesores_list, key=lambda user: user.id).id+1)