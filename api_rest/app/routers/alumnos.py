from fastapi import APIRouter, HTTPException
from db.models.alumno import Alumno
from db.models.colegio import Colegio
from db.client import db_client
from db.schemas.alumno import alumno_schema, alumnos_schema
from db.schemas.colegio import colegio_schema, colegios_schema
from bson import ObjectId


router = APIRouter(prefix="/alumnos", tags=["alumnos"])


cursos = ["1ESO", "2ESO", "3ESO", "4ESO", "1BACH", "2BACH"]

# Metodo get
@router.get("/", response_model=list[Alumno])
async def alumnos():
    return alumnos_schema(db_client.examen.alumnos.find())


# Método get tipo query??


# Metodo post
@router.post("/", response_model=Alumno, status_code=201)
async def add_alumno(alumno: Alumno):

    # Buscamos y almacenamos el colegio
    colegio = search_colegio_id(alumno.id_colegio)

    # Si el colegio indicado existe
    if (colegio):    

        if (alumno.curso not in cursos):
            raise HTTPException(status_code=409, detail="El curso no es válido")

        alumno_dict = alumno.model_dump()
        del alumno_dict["id"]

        # Añadimos el alumno a nuestra base de datos
        id = db_client.examen.alumnos.insert_one(alumno_dict).inserted_id

        # Añadimos el campo id a nuestro diccionario
        alumno_dict["id"] = str(id)

        # Devolvemos el alumno añadido
        return Alumno(**alumno_dict)
    else:
        raise HTTPException(status_code=409, detail="El colegio indicado no existe")
    

# Metodo put
@router.put("/{id}", response_model=Alumno)
async def modify_asignatura(id: str, new_alumno: Alumno):

    # Buscamos y almacenamos el colegio
    colegio = search_colegio_id(new_alumno.id_colegio)

    if (colegio):
        # Convertimos el alumno a un diccionario
        alumno_dict = new_alumno.model_dump()

        # Eliminamos el id en caso de que venga porque no puede cambiar
        del alumno_dict["id"]   
        try:
            db_client.examen.alumnos.find_one_and_replace({"_id":ObjectId(id)}, alumno_dict)
            return search_alumno_id(id)    
        except:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
    else:
        raise HTTPException(status_code=404, detail="El colegio indicado no existe")    
    

# Metodo delete
@router.delete("/{id}", response_model=Alumno)
async def delete_alumno(id:str):
    found = db_client.examen.alumnos.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return Alumno(**alumno_schema(found))



# Metodo para buscar alumno por Id
def search_alumno_id(id: str):    
    try:
        alumno = alumno_schema(db_client.examen.alumnos.find_one({"_id":ObjectId(id)}))
        return Alumno(**alumno)
    except:
        return {"error": "El colegio no existe"}
    

# Metodo getById para validar que el colegio existe
def search_colegio_id(id: str):    
    try:
        colegio = colegio_schema(db_client.examen.colegios.find_one({"_id":ObjectId(id)}))
        return Colegio(**colegio)
    except:
        return {"error": "El colegio no existe"}