from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from db.models.asignatura import Asignatura
from db.client import db_client
from db.schemas.asignatura import asignatura_schema, asignaturas_schema
from bson import ObjectId
from routers.asignaturas import asignaturas_list 


router = APIRouter(prefix="/asignaturasdb", tags=["asignaturasdb"])


@router.get("/", response_model=list[Asignatura])
async def asignaturas():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return asignaturas_schema(db_client.test.asignaturas.find())

# Método get tipo query. Sólo busca por id
@router.get("", response_model=Asignatura)
async def asignatura(id: str):
    return search_asignatura_id(id)


# Método get por id
@router.get("/{id}", response_model=Asignatura)
async def asignatura(id: str):
    return search_asignatura_id(id)


@router.post("/", response_model=Asignatura, status_code=201)
async def add_asignatura(asignatura: Asignatura):
    #print("dentro de post")
    if type(search_asignatura(asignatura.titulo)) == Asignatura:
        raise HTTPException(status_code=409, detail="Asignatura already exists")
    
    asignatura_dict = asignatura.model_dump()
    del asignatura_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id = db_client.test.asignaturas.insert_one(asignatura_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    asignatura_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Asignatura(**asignatura_dict)
    
@router.put("/{id}", response_model=Asignatura)
async def modify_asignatura(id: str, new_asignatura: Asignatura):
    # Convertimos el usuario a un diccionario
    asignatura_dict = new_asignatura.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del asignatura_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.asignaturas.find_one_and_replace({"_id":ObjectId(id)}, asignatura_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_asignatura_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Asignatura not found")
    

@router.delete("/{id}", response_model=Asignatura)
async def delete_asignatura(id:str):
    found = db_client.test.asignaturas.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Asignatura not found")
    return Asignatura(**asignatura_schema(found))
   
   
# El id de la base de datos es un string, ya no es un entero
def search_asignatura_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        asignatura = asignatura_schema(db_client.test.asignaturas.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Asignatura(**asignatura)
    except:
        return {"error": "Asignatura not found"}


def search_asignatura(titulo: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        asignatura = asignatura_schema(db_client.test.users.find_one({"titulo":titulo}))
        return Asignatura(**asignatura)
    except:
        return {"error": "Asignatura not found"}





def next_id():
    # Calculamos el usuario con el id más alto 
    # y le sumamos 1 a su id
    return (max(asignatura.id for asignatura in asignaturas_list))+1

