from typing import Optional 
from pydantic import BaseModel

# Entidad tienda
class Tienda(BaseModel):
    id: Optional[str] = None
    domicilio: str
    telefono: int
    precio_alquiler: int