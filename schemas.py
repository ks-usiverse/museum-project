from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    user_id: int
    username: str
    password: str

    class Config:
        orm_mode = True

class QuizSchema(BaseModel):
    quiz_id: int
    question_text: str
    image_url: Optional[str] = None
    hint: Optional[str] = None
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_answer: str

    class Config:
        orm_mode = True

class MapSchema(BaseModel):
    map_point_id: int
    location_name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class UserQuizProgressSchema(BaseModel):
    progress_id: int
    user_id: int
    quiz_id: int
    map_point_id: int
    is_correct: bool

    class Config:
        orm_mode = True