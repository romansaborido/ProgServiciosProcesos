def profesor_schema(profesor) -> dict:
    return {
        "id": str(profesor["_id"]),
        "titulo": profesor["titulo"],
        "num_horas": profesor["num_horas"],
        "id_profesor": profesor["id_profesor"]
    }

def profesor_schema(profesores) -> list:
    return [profesor_schema(profesor) for profesor in profesores]