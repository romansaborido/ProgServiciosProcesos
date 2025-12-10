from fastapi import APIRouter, HTTPException
from db.models.profesor import Profesor
from db.schemas.profesor import profesor_schema, profesores_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/profesoresdb", tags=["profesoresdb"])


@router.get("/", response_model=list[Profesor])
async def profesores():
    # El método find() sin parámetros devuelve todos los registros
    # de la base de datos
    return profesores_schema(db_client.test.profesores.find())


# Método get tipo query. Sólo busca por id
@router.get("", response_model=Profesor)
async def profesor(id: str):
    return search_profesor_id(id)


# Método get por id
@router.get("/{id}", response_model=Profesor)
async def profesor(id: str):
    return search_profesor_id(id)


@router.post("/", response_model=Profesor, status_code=201)
async def add_profesor(profesor: Profesor):
    #print("dentro de post")
    if type(search_profesor(profesor.nombre, profesor.apellidos)) == Profesor:
        raise HTTPException(status_code=409, detail="Profesor already exists")
    
    profesor_dict = profesor.model_dump()
    del profesor_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id = db_client.test.profesores.insert_one(profesor_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    profesor_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Profesor(**profesor_dict)


@router.put("/{id}", response_model=Profesor)
async def modify_profesor(id: str, new_profesor: Profesor):
    # Convertimos el usuario a un diccionario
    profesor_dict = new_profesor.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del profesor_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.profesores.find_one_and_replace({"_id":ObjectId(id)}, profesor_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_profesor_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Profesor not found")
    

@router.delete("/{id}", response_model=Profesor)
async def delete_profesor(id:str):
    found = db_client.test.profesores.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return Profesor(**profesor_schema(found)) 



# El id de la base de datos es un string, ya no es un entero
def search_profesor_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        profesor = profesor_schema(db_client.test.profesores.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Profesor(**profesor)
    except:
        return {"error": "Profesor not found"}


def search_profesor(nombre: str, apellidos: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        profesor = profesor_schema(db_client.test.profesores.find_one({"nombre":nombre, "apellidos":apellidos}))
        return Profesor(**profesor)
    except:
        return {"error": "Profesor not found"}