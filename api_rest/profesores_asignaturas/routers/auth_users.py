from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import *


# Algoritmo de encriptacion
ALGORITM = "HS256"

# Duracion del token
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Clave que utilizara como semilla para generar el token
SECRET_KEY = "d19e34c2b8f5a71e0f6c9b24d7a3e85f9c41ab72de63f08e1d0b5c97e4f20a8b"

# Objeto que utilizaremos para el hash de la contraseña
password_hash = PasswordHash.recommended()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter()


class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "romansc" : {
        "username" : "romansc",
        "fullname" : "Roman Saborido",
        "email" : "roman.saborido@iesnervion.es",
        "disabled" : False,
        "password" : "hola1234"
    },
    "rubencf" : {
        "username": "rubencf",
        "fullname": "Ruben Carrasco",
        "email": "ruben.carrasco@iesnervion.es",
        "disabled": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$eA+9F35OVhXZn4TGktsKQg$l+5CbCy25KN9gYWCN+u8Sj3bdfdbTHl1xXCWmNlBbwU"
    }
}



@router.post("/register", status_code=201, response_model=UserDB)
def add_user(user: UserDB):
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user
        return user
    else:
        raise HTTPException(status_code=409, detail="User already exists")


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if user:
        # Si el usuario existe, comprobamos la contraseña
        if password_hash.verify(form.password, user["password"]):
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = {"sub": user.username, "exp":expire}
            # Generamos el tokekn
            token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITM)
            return {"access_token":token, "token_type":"bearer"}
    raise HTTPException(status_code=401, detail="Usuario y/o contraseña incorrectos")



