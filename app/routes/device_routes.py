from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_admin, require_admin_or_support
from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.schemas.device_schema import DeviceCreate, DeviceResponse, DeviceUpdate
from app.services.device_service import (
    create_device,
    delete_device,
    get_all_devices,
    get_device_by_id,
    get_device_by_serial,
    update_device,
)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
)
def list_devices(
    device_type: Optional[str] = None,
    brand: Optional[str] = None,
    is_available: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_all_devices(db, device_type, brand, is_available, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID",
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Requiere rol admin o support.",
)
def create_new_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    existing = get_device_by_serial(db, device.serial_number)
    if existing:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    return create_device(db, device.model_dump())


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    description="Requiere rol admin o support.",
)
def replace_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    if device_data.serial_number:
        existing = get_device_by_serial(db, device_data.serial_number)
        if existing and existing.id != device_id:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado por otro dispositivo")

    return update_device(db, device_id, device_data.model_dump(exclude_unset=True))


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente",
    description="Requiere rol admin o support.",
)
def partial_update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_support),
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    update_data = device_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    if "serial_number" in update_data:
        existing = get_device_by_serial(db, update_data["serial_number"])
        if existing and existing.id != device_id:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado por otro dispositivo")

    return update_device(db, device_id, update_data)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Requiere rol admin.",
)
def remove_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = delete_device(db, device_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)