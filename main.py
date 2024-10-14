# main.py

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Set up static file serving
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check for duplicate IDs
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        if existing_user.password == password:
            response = RedirectResponse(f"/main?user_id={existing_user.user_id}", status_code=303)
            return response
        else:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid password."})
    else:
        # Create a new user
        new_user = models.User(username=username, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        response = RedirectResponse(f"/main?user_id={new_user.user_id}", status_code=303)
        return response

@app.get("/main", response_class=HTMLResponse)
def main_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        return RedirectResponse("/", status_code=303)
    progress = db.query(models.UserQuizProgress).filter(models.UserQuizProgress.user_id == user_id, models.UserQuizProgress.is_correct == True).all()
    completed_quizzes = [p.quiz_id for p in progress]

    next_quiz_id = max(completed_quizzes, default=0) + 1

    total_quizzes = db.query(models.Quiz).count()

    return templates.TemplateResponse("main.html", {"request": request, "user_id": user_id, "completed_quizzes": completed_quizzes, "next_quiz_id": next_quiz_id, "total_quizzes": total_quizzes})

@app.get("/quiz/{quiz_id}", response_class=HTMLResponse)
def get_quiz(request: Request, quiz_id: int, user_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if not quiz:
        return HTMLResponse("Can't find the quiz.", status_code=404)
    return templates.TemplateResponse("quiz.html", {"request": request, "quiz": quiz, "user_id": user_id})

@app.post("/quiz/{quiz_id}/submit", response_class=HTMLResponse)
def submit_quiz(request: Request, quiz_id: int, user_id: int, selected_option: str = Form(...), db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.quiz_id == quiz_id).first()
    if not quiz:
        return HTMLResponse("Can't find the quiz.", status_code=404)
    is_correct = selected_option == quiz.correct_answer
    # Update user progress
    progress = db.query(models.UserQuizProgress).filter(models.UserQuizProgress.user_id == user_id, models.UserQuizProgress.quiz_id == quiz_id).first()
    if progress:
        progress.is_correct = is_correct
    else:
        progress = models.UserQuizProgress(user_id=user_id, quiz_id=quiz_id, is_correct=is_correct)
        db.add(progress)
    db.commit()
    if is_correct:
        # Redirect to the main page
        response = RedirectResponse(f"/main?user_id={user_id}", status_code=303)
        return response
    else:
        # display a message if incorrect
        error = "This is incorrect, please try again."
        return templates.TemplateResponse("quiz.html", {"request": request, "quiz": quiz, "user_id": user_id, "error": error})
