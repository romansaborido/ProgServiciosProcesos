def empleado_schema(empleado) -> dict:
    return {
        "id": str(empleado["_id"]),
        "nombre": empleado["nombre"],
        "apellidos": empleado["apellidos"],
        "telefono": empleado["telefono"],
        "correo": empleado["correo"],
        "num_cuenta": empleado["num_cuenta"],
        "id_tienda": empleado["id_tienda"]
    }

def empleados_schema(empleados) -> list:
    return [empleado_schema(empleado) for empleado in empleados]