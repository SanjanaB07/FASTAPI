from sqlalchemy.orm import Session
import models


def create(db, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_all(db: Session, model):
    return db.query(model).all()


def get_by_id(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()


def delete(db: Session, obj):
    db.delete(obj)
    db.commit()
