from fastapi import APIRouter, HTTPException, Query, Response
from typing import List, Optional

from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

# Base de datos simulada
users_db = [
    {
        "id": 1,
        "name": "Juan Perez",
        "email": "juan@example.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Maria Lopez",
        "email": "maria@example.com",
        "role": "support",
        "is_active": False
    }
]


# GET /users
@router.get("/users", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    result = users_db

    # Filtrar por rol
    if role:
        result = [user for user in result if user["role"] == role]

    # Filtrar por estado
    if is_active is not None:
        result = [user for user in result if user["is_active"] == is_active]

    return result


# GET /users/{user_id}
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# POST /users
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, response: Response):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    # Validar correo duplicado
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    # Crear nuevo usuario
    new_user = {
        "id": len(users_db) + 1,
        **user.model_dump()
    }

    users_db.append(new_user)

    return new_user