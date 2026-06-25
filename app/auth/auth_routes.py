from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.auth.security import create_access_token
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.auth_schema import Token, UserAuthResponse, UserLogin, UserRegister

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Límite: 3 peticiones/minuto.",
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    return auth_service.register_user(db, user_data)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Retorna token JWT. Límite: 5 peticiones/minuto.",
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    user = auth_service.authenticate_user(db, login_data)
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserAuthResponse,
    summary="Obtener usuario autenticado",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user