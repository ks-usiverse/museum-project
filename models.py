from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    quiz_progress = relationship("UserQuizProgress", back_populates="user")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    quiz_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    hint = Column(Text, nullable=True)
    option_1 = Column(String, nullable=False)
    option_2 = Column(String, nullable=False)
    option_3 = Column(String, nullable=False)
    option_4 = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)

    progress_records = relationship("UserQuizProgress", back_populates="quiz")

class Map(Base):
    __tablename__ = "maps"
    
    map_point_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    progress_records = relationship("UserQuizProgress", back_populates="map")

class UserQuizProgress(Base):
    __tablename__ = "user_quiz_progress"
    
    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"), nullable=False)
    map_point_id = Column(Integer, ForeignKey("maps.map_point_id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="quiz_progress")
    quiz = relationship("Quiz", back_populates="progress_records")
    map = relationship("Map", back_populates="progress_records")