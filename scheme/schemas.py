def one_user(user)->dict:
    return {
        "id": str(user["_id"]),
        "name": user["username"],
        "email": user["email"],
        "password": user["password"],
        "disabled": user.get("disabled",False) 
    }

def many_users(users)->list:
    return [one_user(user) for user in users]