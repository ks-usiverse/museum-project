from sqlalchemy.orm import Session
from models import Museum

def get_museums(db: Session):
    return db.query(Museum).all()