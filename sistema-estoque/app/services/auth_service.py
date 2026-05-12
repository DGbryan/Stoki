from sqlalchemy.orm import Session
from app.database.models import Operator

def authenticate_operator(db: Session, email: str, password: str) -> Operator:
    return db.query(Operator).filter(
        Operator.email == email,
        Operator.password == password
    ).first()

def register_operator(db: Session, name: str, email: str, password: str) -> Operator:
    new_op = Operator(
        name=name,
        email=email,
        password=password
    )
    db.add(new_op)
    db.commit()
    db.refresh(new_op)
    return new_op

def reset_password(db: Session, email: str) -> bool:
    operator = db.query(Operator).filter(Operator.email == email).first()
    if operator:
        operator.password = "1234"
        db.commit()
        return True
    return False

def init_default_user(db: Session):
    operator = db.query(Operator).filter(Operator.email == "unilux@teste.com").first()
    if not operator:
        register_operator(db, "Unilux Admin", "unilux@teste.com", "1234")
