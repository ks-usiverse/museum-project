from sqlalchemy.orm import Session
from models import User, Quiz, Map, UserQuizProgress

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_quizzes(db: Session):
    return db.query(Quiz).all()

def get_quiz(db: Session, quiz_id: int):
    return db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()

def get_maps(db: Session):
    return db.query(Map).all()

def get_map(db: Session, map_point_id: int):
    return db.query(Map).filter(Map.map_point_id == map_point_id).first()

def get_user_quiz_progress(db: Session, user_id: int):
    return db.query(UserQuizProgress).filter(UserQuizProgress.user_id == user_id).all()

def add_user_quiz_progress(db: Session, progress_data: dict):
    progress = UserQuizProgress(**progress_data)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress