from fastapi import APIRouter, HTTPException
from models.Empleado import Empleado
from bd.client import db_client
from bd.schemas.Empleado import empleado_schema, empleados_schema
from bson import ObjectId


router = APIRouter(prefix="/empleadosbd", tags=["empleadosbd"])


@router.get("/", response_model=list[Empleado])
async def empleados():
    return empleados_schema(db_client.test.empleados.find())


# Método get por id
@router.get("/{id}", response_model=Empleado)
async def empleado(id: str):
    return search_empleado_id(id)


@router.post("/", response_model=Empleado, status_code=201)
async def add_empleado(empleado: Empleado):
    #print("dentro de post")
    if type(search_empleado(empleado.nombre, empleado.apellidos)) == Empleado:
        raise HTTPException(status_code=409, detail="Empleado already exists")
    
    empleado_dict = empleado.model_dump()
    del empleado_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id = db_client.test.empleados.insert_one(empleado_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    empleado_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Empleado(**empleado_dict)
    
@router.put("/{id}", response_model=Empleado)
async def modify_empleado(id: str, new_empleado: Empleado):
    # Convertimos el usuario a un diccionario
    empleado_dict = new_empleado.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del empleado_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.empleados.find_one_and_replace({"_id":ObjectId(id)}, empleado_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_empleado_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Empleado not found")
    

@router.delete("/{id}", response_model=Empleado)
async def delete_empleado(id:str):
    found = db_client.test.empleados.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Empleado not found")
    return Empleado(**empleado_schema(found))
   
   
# El id de la base de datos es un string, ya no es un entero
def search_empleado_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        empleado = empleado_schema(db_client.test.empleados.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Empleado(**empleado)
    except:
        return {"error": "Empleado not found"}


def search_empleado(nombre: str, apellidos: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        empleado = empleado_schema(db_client.test.empleados.find_one({"nombre":nombre, "apellidos":apellidos}))
        return Empleado(**empleado)
    except:
        return {"error": "Empleado not found"}
    