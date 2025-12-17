def colegio_schema(colegio) -> dict:
    return {
        "id": str(colegio["_id"]),
        "nombre": str(colegio["nombre"]),
        "distrito": str(colegio["distrito"]),
        "tipo": str(colegio["tipo"]),
        "direccion": str(colegio["direccion"])
    }

def colegios_schema(colegios) -> list:
    return [colegio_schema(colegio) for colegio in colegios]