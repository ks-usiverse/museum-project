from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import UserSchema, QuizSchema, MapSchema, UserQuizProgressSchema
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
    return {"Hello": "Not World"}

@app.get("/users", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        logging.error(f"User with id {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/quizzes", response_model=List[QuizSchema])
def read_quizzes(db: Session = Depends(get_db)):
    quizzes = crud.get_quizzes(db)
    return quizzes

@app.get("/quizzes/{quiz_id}", response_model=QuizSchema)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = crud.get_quiz(db, quiz_id)
    if quiz is None:
        logging.error(f"Quiz with id {quiz_id} not found.")
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@app.get("/maps", response_model=List[MapSchema])
def read_maps(db: Session = Depends(get_db)):
    maps = crud.get_maps(db)
    return maps

@app.get("/maps/{map_point_id}", response_model=MapSchema)
def read_map(map_point_id: int, db: Session = Depends(get_db)):
    map_point = crud.get_map(db, map_point_id)
    if map_point is None:
        logging.error(f"Map point with id {map_point_id} not found.")
        raise HTTPException(status_code=404, detail="Map point not found")
    return map_point

@app.get("/users/{user_id}/progress", response_model=List[UserQuizProgressSchema])
def read_user_quiz_progress(user_id: int, db: Session = Depends(get_db)):
    progress = crud.get_user_quiz_progress(db, user_id)
    return progress

@app.post("/users/progress", response_model=UserQuizProgressSchema)
def create_user_quiz_progress(progress_data: UserQuizProgressSchema, db: Session = Depends(get_db)):
    progress = crud.add_user_quiz_progress(db, progress_data.dict())
    return progress