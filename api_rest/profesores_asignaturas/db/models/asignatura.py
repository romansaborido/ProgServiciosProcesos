from typing import Optional 
from pydantic import BaseModel

# Entidad asignatura
class Asignatura(BaseModel):
    id: Optional[str] = None
    titulo: str
    num_horas: int
    id_profesor: int