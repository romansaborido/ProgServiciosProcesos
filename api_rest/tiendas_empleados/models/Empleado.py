from typing import Optional 
from pydantic import BaseModel

# Entidad empleado
class Empleado(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellidos: str
    telefono: int
    correo: str
    num_cuenta: str
    id_tienda: int