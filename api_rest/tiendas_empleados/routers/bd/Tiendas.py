from fastapi import APIRouter, HTTPException
from models.Tienda import Tienda
from bd.client import db_client
from bd.schemas.Tienda import tienda_schema, tiendas_schema
from bson import ObjectId


router = APIRouter(prefix="/tiendasbd", tags=["tiendasbd"])


@router.get("/", response_model=list[Tienda])
async def tiendas():
    return tiendas_schema(db_client.test.tiendas.find())


# Método get tipo query. Sólo busca por id
@router.get("", response_model=Tienda)
async def tienda(id: str):
    return search_tienda_id(id)


# Método get por id
@router.get("/{id}", response_model=Tienda)
async def tienda(id: str):
    return search_tienda_id(id)


@router.post("/", response_model=Tienda, status_code=201)
async def add_tienda(tienda: Tienda):
    #print("dentro de post")
    if type(search_tienda(tienda.domicilio)) == Tienda:
        raise HTTPException(status_code=409, detail="Tienda already exists")
    
    tienda_dict = tienda.model_dump()
    del tienda_dict["id"]
    # Añadimos el usuario a nuestra base de datos
    # También podemos obtner con inserted_id el id que la base de datos
    # ha generado para nuestro usuario
    id = db_client.test.tiendas.insert_one(tienda_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario. Hay que hacerle un cast
    # a string puesto que el id en base de datos se almacena como un objeto,
    # no como un string
    tienda_dict["id"] = str(id)

    # La respuesta de nuestro método es el propio usuario añadido
    # Creamos un objeto de tipo User a partir del diccionario user_dict
    return Tienda(**tienda_dict)
    
@router.put("/{id}", response_model=Tienda)
async def modify_tienda(id: str, new_tienda: Tienda):
    # Convertimos el usuario a un diccionario
    tienda_dict = new_tienda.model_dump()
    # Eliminamos el id en caso de que venga porque no puede cambiar
    del tienda_dict["id"]   
    try:
        # Buscamos el id en la base de datos y le pasamos el diccionario con los datos
        # a modificar del usuario
        db_client.test.tiendas.find_one_and_replace({"_id":ObjectId(id)}, tienda_dict)
        # Buscamos el objeto en base de datos y lo retornamos, así comprobamos que efectivamente
        # se ha modificado
        return search_tienda_id(id)    
    except:
        raise HTTPException(status_code=404, detail="Tienda not found")
    

@router.delete("/{id}", response_model=Tienda)
async def delete_tienda(id:str):
    found = db_client.test.tiendas.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        raise HTTPException(status_code=404, detail="Tienda not found")
    return Tienda(**tienda_schema(found))
   
   
# El id de la base de datos es un string, ya no es un entero
def search_tienda_id(id: str):    
    # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
    # así que la controlamos
    try:
        # El id en base de datos no se guarda como un string, sino que es un objeto 
        # Realizamos la conversión    
        tienda = tienda_schema(db_client.test.tiendas.find_one({"_id":ObjectId(id)}))
        # Necesitamos convertirlo a un objeto User. 
        return Tienda(**tienda)
    except:
        return {"error": "Tienda not found"}


def search_tienda(direccion: str):
    # La búsqueda me devuelve un objeto del tipo de la base de datos.
    # Necesitamos convertirlo a un objeto User. 
    try:
        # Si algo va mal en la búsqueda dentro de la base de datos se lanzará una excepción,
        # así que la controlamos
        tienda = tienda_schema(db_client.test.tiendas.find_one({"direccion":direccion}))
        return Tienda(**tienda)
    except:
        return {"error": "Tienda not found"}
    

