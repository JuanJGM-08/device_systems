from sqlalchemy.orm import Session

from app.models.user_model import User


def get_all_users(
    db: Session,
    role=None,
    is_active=None
):
    query = db.query(User)

    if role:
        query = query.filter(
            User.role == role
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    return query.all()


def get_user_by_id(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_user_by_email(
    db: Session,
    email: str
):
    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
    db: Session,
    user_data
):
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user_id: int,
    user_data
):
    user = get_user_by_id(
        db,
        user_id
    )

    for key, value in user_data.items():
        setattr(
            user,
            key,
            value
        )

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user_id: int
):
    user = get_user_by_id(
        db,
        user_id
    )

    db.delete(user)
    db.commit()