from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.services.user_service import (
    get_user_by_id,
    get_user_by_email
)


def get_user_or_404(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


def validate_email_unique(
    email: str,
    db: Session,
    user_id: int = None
):
    user = get_user_by_email(
        db,
        email
    )

    if user and user.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Correo electrónico duplicado"
        )