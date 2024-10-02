from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import MuseumSchema, ExhibitSchema
from typing import List
import crud
import models
import logging

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

logging.basicConfig(filename='app.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(message)s')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/museums", response_model=List[MuseumSchema])
def read_museums(db: Session = Depends(get_db)):
    museums = crud.get_museums(db)
    return museums

@app.get("/exhibits", response_model=List[ExhibitSchema])
def read_exhibits(db: Session = Depends(get_db)):
    exhibits = crud.get_exhibits(db)
    return exhibits

@app.get("/exhibits/{exhibit_id}", response_model=ExhibitSchema)
def read_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit = crud.get_exhibit(db, exhibit_id)
    if exhibit is None:
        print(f"Exhibit with id {exhibit_id} not found.")
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit