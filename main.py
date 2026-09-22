from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

# 서버 시작 시 DB 테이블 자동 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class TodoCreate(BaseModel):
    title: str

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "v2"}

@app.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()