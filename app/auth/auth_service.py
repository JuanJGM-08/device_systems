"""
auth_service.py
---------------
Lógica de negocio para autenticación: registro y login de usuarios.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import get_password_hash, verify_password
from app.models.user_model import User
from app.schemas.auth_schema import UserLogin, UserRegister


def register_user(db: Session, user_data: UserRegister) -> User:
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    hashed = get_password_hash(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed,
        role=user_data.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, login_data: UserLogin) -> User:
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return user