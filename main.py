from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import MuseumSchema
from typing import List
import crud
import models
import init_db

init_db.init_db()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/museums", response_model=List[MuseumSchema])
def read_museums(db: Session = Depends(get_db)):
    museums = crud.get_museums(db)
    return museums