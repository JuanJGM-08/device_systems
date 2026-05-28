from fastapi import APIRouter, HTTPException, Depends, Response, status
from typing import Optional

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
    is_active: Optional[bool] = None
):
    users = get_all_users()

    if role:
        users = [user for user in users if user["role"] == role]

    if is_active is not None:
        users = [
            user for user in users
            if user["is_active"] == is_active
        ]

    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID"
)
def get_user(user=Depends(get_user_or_404)):
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario"
)
def create_new_user(user: UserCreate):

    validate_email_unique(user.email)

    return create_user(user.model_dump())


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo"
)
def replace_user(
    user_data: UserCreate,
    user=Depends(get_user_or_404)
):

    validate_email_unique(
        user_data.email,
        user["id"]
    )

    updated_user = update_user(
        user["id"],
        user_data.model_dump()
    )

    return updated_user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente"
)
def partial_update_user(
    user_data: UserUpdate,
    user=Depends(get_user_or_404)
):

    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No se enviaron datos para actualizar"
        )

    if "email" in update_data:
        validate_email_unique(
            update_data["email"],
            user["id"]
        )

    updated_user = update_user(
        user["id"],
        update_data
    )

    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario"
)
def remove_user(user=Depends(get_user_or_404)):

    delete_user(user["id"])

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )