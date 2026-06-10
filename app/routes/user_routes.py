from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate
)

from app.services.user_service import (
    get_all_users,
    create_user,
    update_user,
    delete_user
)

from app.dependencies.user_dependencies import (
    get_user_or_404,
    validate_email_unique
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios registrados"
)
def list_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return get_all_users(
        db,
        role,
        is_active
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID"
)
def get_user(
    user=Depends(get_user_or_404)
):
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario"
)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    validate_email_unique(
        user.email,
        db
    )

    return create_user(
        db,
        user.model_dump()
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo"
)
def replace_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(get_user_or_404)
):
    validate_email_unique(
        user_data.email,
        db,
        user.id
    )

    return update_user(
        db,
        user.id,
        user_data.model_dump()
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente"
)
def partial_update_user(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_user_or_404)
):
    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    if "email" in update_data:
        validate_email_unique(
            update_data["email"],
            db,
            user.id
        )

    return update_user(
        db,
        user.id,
        update_data
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario"
)
def remove_user(
    db: Session = Depends(get_db),
    user=Depends(get_user_or_404)
):
    delete_user(
        db,
        user.id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )