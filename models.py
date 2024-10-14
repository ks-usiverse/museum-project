from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    progress = relationship("UserQuizProgress", back_populates="user")

class Quiz(Base):
    __tablename__ = "quizzes"

    quiz_id = Column(Integer, primary_key=True)
    question_text = Column(String)
    image_url = Column(String)
    hint = Column(String)
    option_1 = Column(String)
    option_2 = Column(String)
    option_3 = Column(String)
    option_4 = Column(String)
    correct_answer = Column(String)

class UserQuizProgress(Base):
    __tablename__ = "user_quiz_progress"

    progress_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'))
    is_correct = Column(Boolean)

    user = relationship("User", back_populates="progress")
    quiz = relationship("Quiz")