from fastapi import APIRouter, HTTPException
from db.models.colegio import Colegio
from db.client import db_client
from db.schemas.colegio import colegio_schema, colegios_schema
from bson import ObjectId


router = APIRouter(prefix="/colegios", tags=["colegios"])


# Metodo get
@router.get("/", response_model=list[Colegio])
async def colegio():
    return colegios_schema(db_client.examen.colegios.find())


# Metodo get por id
@router.get("/{id}", response_model=Colegio)
async def colegio(id: str):
    colegio = search_colegio_id(id)
    if (colegio):
        return colegio
    else:
        raise HTTPException(status_code=404, detail="El colegio no existe")    


# Metodo post
@router.post("/", response_model=Colegio, status_code=201)
async def add_colegio(colegio: Colegio):

    # Comprobamos que el colegio no exista
    if type(search_colegio(colegio.direccion)) == Colegio:
        raise HTTPException(status_code=409, detail="El colegio ya existe")
    
    # Comprobamos que el tipo es valido, si no lo es lanzamos excepcion
    if (colegio.tipo != "publico" and colegio.tipo != "concertado" and colegio.tipo != "privado"):
        raise HTTPException(status_code=400, detail="El tipo del colegio no es válido")

    colegio_dict = colegio.model_dump()
    del colegio_dict["id"]

    # Añadimos el colegio a nuestra base de datos
    id = db_client.examen.colegios.insert_one(colegio_dict).inserted_id

    # Añadimos el campo id a nuestro diccionario
    colegio_dict["id"] = str(id)

    # Devolvemos el colegio añadido
    return Colegio(**colegio_dict)
    
   
# Metodo eliminar colegio
@router.delete("/{id}", response_model=Colegio)
async def delete_colegio(id:str):
    found = db_client.examen.colegios.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    return Colegio(**colegio_schema(found))

# Terminar   



# Metodo buscar colegio por id
def search_colegio_id(id: str):    
    try:  
        colegio = colegio_schema(db_client.examen.colegios.find_one({"_id":ObjectId(id)}))
        return Colegio(**colegio)
    except:
        return {"error": "Colegio no encontrado"}


# Metodo buscar colegio por direccion
def search_colegio(direccion: str):
    try:
        colegio = colegio_schema(db_client.examen.colegios.find_one({"direccion":direccion}))
        return Colegio(**colegio)
    except:
        return {"error": "Colegio no encontrado"}