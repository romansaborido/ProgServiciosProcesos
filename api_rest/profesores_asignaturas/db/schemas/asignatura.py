def asignatura_schema(asignatura) -> dict:
    return {
        "id": str(asignatura["_id"]),
        "titulo": asignatura["titulo"],
        "num_horas": asignatura["num_horas"],
        "id_profesor": asignatura["id_profesor"]
    }

def asignaturas_schema(asignaturas) -> list:
    return [asignatura_schema(asignatura) for asignatura in asignaturas]