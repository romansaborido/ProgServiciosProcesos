def alumno_schema(alumno) -> dict:
    return {
        "id": str(alumno["_id"]),
        "nombre": str(alumno["nombre"]),
        "apellidos": str(alumno["apellidos"]),
        "fecha_nacimiento": str(alumno["fecha_nacimiento"]),
        "curso": str(alumno["curso"]),
        "repetidor": bool(alumno["repetidor"]),
        "id_colegio": str(alumno["id_colegio"])

    }

def alumnos_schema(alumnos) -> list:
    return [alumno_schema(alumno) for alumno in alumnos]