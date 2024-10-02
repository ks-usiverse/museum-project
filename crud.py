from sqlalchemy.orm import Session
from models import Museum, Exhibit

def get_museums(db: Session):
    return db.query(Museum).all()

def get_exhibits(db: Session):
    return db.query(Exhibit).all()

def get_exhibit(db: Session, exhibit_id: int):
    return db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()