from typing import Optional 
from pydantic import BaseModel

# Entidad user
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool