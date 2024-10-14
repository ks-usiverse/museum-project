import json
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Quiz

def load_data():
    with open('initial_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    db = SessionLocal()

    for quiz_data in data["quizzes"]:
        quiz = Quiz(
            quiz_id=quiz_data["quiz_id"],
            question_text=quiz_data["question_text"],
            image_url=quiz_data["image_url"],
            hint=quiz_data["hint"],
            option_1=quiz_data["option_1"],
            option_2=quiz_data["option_2"],
            option_3=quiz_data["option_3"],
            option_4=quiz_data["option_4"],
            correct_answer=quiz_data["correct_answer"]
        )
        db.add(quiz)

    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    load_data()