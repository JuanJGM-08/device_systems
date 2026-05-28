from fastapi import HTTPException
from app.data.users_db import users_db
from app.services.user_service import get_user_by_id


def get_user_or_404(user_id: int):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


def validate_email_unique(email: str, user_id: int = None):
    for user in users_db:
        if user["email"] == email and user["id"] != user_id:
            raise HTTPException(
                status_code=400,
                detail="Correo electrónico duplicado"
            )