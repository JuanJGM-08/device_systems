from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.services.user_service import get_user_by_id
from app.services.device_service import get_device_by_id


def get_all_loans(
    db: Session,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    query = db.query(Loan)

    if user_id:
        query = query.filter(Loan.user_id == user_id)

    if device_id:
        query = query.filter(Loan.device_id == device_id)

    if status:
        query = query.filter(Loan.status == status)

    if user_email:
        query = query.join(User).filter(User.email == user_email)

    if device_type:
        query = query.join(Device).filter(Device.device_type == device_type)

    return query.all()


def get_loans_with_details(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    query = db.query(Loan).join(User).join(Device)

    if status:
        query = query.filter(Loan.status == status)

    if user_email:
        query = query.filter(User.email == user_email)

    if device_type:
        query = query.filter(Device.device_type == device_type)

    return query.all()


def get_loan_by_id(db: Session, loan_id: int):
    return db.query(Loan).filter(Loan.id == loan_id).first()


def get_user_loans(db: Session, user_id: int):
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def get_device_loans(db: Session, device_id: int):
    return db.query(Loan).filter(Loan.device_id == device_id).all()


def create_loan(db: Session, loan_data: dict):
    # Validar usuario
    user = get_user_by_id(db, loan_data["user_id"])
    if not user:
        return None

    # Validar dispositivo
    device = get_device_by_id(db, loan_data["device_id"])
    if not device:
        return None

    if not device.is_available:
        return None  # Dispositivo no disponible

    # Crear préstamo
    loan = Loan(**loan_data)
    db.add(loan)

    # Marcar dispositivo como no disponible
    device.is_available = False

    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        return None

    if loan.status == "returned":
        return None  # Ya devuelto

    loan.status = "returned"
    loan.return_date = datetime.utcnow()

    # Liberar dispositivo
    device = get_device_by_id(db, loan.device_id)
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan


def update_loan(db: Session, loan_id: int, loan_data: dict):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        return None

    for key, value in loan_data.items():
        setattr(loan, key, value)

    db.commit()
    db.refresh(loan)
    return loan


def delete_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)
    if not loan:
        return False

    db.delete(loan)
    db.commit()
    return True