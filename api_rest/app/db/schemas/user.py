def user_schema(user) -> dict:
    return {
        "username": str(user["username"]),
        "fullname": str(user["fullname"]),
        "email": str(user["email"]),
        "disabled": str(user["disabled"]),
        "password": str(user["password"])
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]