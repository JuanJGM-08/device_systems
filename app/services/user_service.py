from app.data.users_db import users_db


def get_all_users():
    return users_db


def get_user_by_id(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    return None


def create_user(user_data):
    new_id = max(user["id"] for user in users_db) + 1 if users_db else 1

    new_user = {
        "id": new_id,
        **user_data
    }

    users_db.append(new_user)

    return new_user


def update_user(user_id: int, user_data):
    user = get_user_by_id(user_id)

    if user:
        user.update(user_data)
        return user

    return None


def delete_user(user_id: int):
    user = get_user_by_id(user_id)

    if user:
        users_db.remove(user)
        return True

    return False