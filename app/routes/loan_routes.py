from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse, LoanUpdate
from app.services.device_service import get_device_by_id
from app.services.loan_service import (
    create_loan,
    delete_loan,
    get_all_loans,
    get_device_loans,
    get_loan_by_id,
    get_loans_with_details,
    get_user_loans,
    return_loan,
    update_loan,
)
from app.services.user_service import get_user_by_id

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"],
)


@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
)
def list_loans(
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_all_loans(db, user_id, device_id, status)


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con detalles (JOIN)",
    description="Requiere rol admin o support.",
)
def list_loans_details(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    return get_loans_with_details(db, status, user_email, device_type)


@router.get(
    "/user/{user_id}",
    response_model=list[LoanResponse],
    summary="Préstamos de un usuario",
)
def list_user_loans(user_id: int, db: Session = Depends(get_db)):
    return get_user_loans(db, user_id)


@router.get(
    "/device/{device_id}",
    response_model=list[LoanResponse],
    summary="Préstamos de un dispositivo",
)
def list_device_loans(device_id: int, db: Session = Depends(get_db)):
    return get_device_loans(db, device_id)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener préstamo por ID",
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Requiere usuario autenticado. Límite: 10 peticiones/minuto.",
)
@limiter.limit("10/minute")
def create_new_loan(
    request: Request,
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    user = get_user_by_id(db, loan.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = get_device_by_id(db, loan.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if not device.is_available:
        raise HTTPException(status_code=400, detail="Dispositivo no disponible para préstamo")

    result = create_loan(db, loan.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Error al crear el préstamo")
    return result


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Requiere rol admin o support.",
)
def return_device(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    result = return_loan(db, loan_id)
    if not result:
        loan = get_loan_by_id(db, loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")
        raise HTTPException(status_code=400, detail="El préstamo ya fue devuelto")
    return result


@router.patch(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Actualizar préstamo",
)
def partial_update_loan(
    loan_id: int,
    loan_data: LoanUpdate,
    db: Session = Depends(get_db),
):
    update_data = loan_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    result = update_loan(db, loan_id, update_data)
    if not result:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return result


@router.delete(
    "/{loan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar préstamo",
)
def remove_loan(loan_id: int, db: Session = Depends(get_db)):
    deleted = delete_loan(db, loan_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)