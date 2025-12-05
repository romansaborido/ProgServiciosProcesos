from typing import Optional 
from pydantic import BaseModel

# Entidad profesor
class Profesor(BaseModel):
    id: Optional[str] = None
    dni: str
    nombre: str
    apellidos: str
    telefono: str
    direccion: str
    cuentaBancaria: str