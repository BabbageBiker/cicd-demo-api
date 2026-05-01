from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from contextlib import asynccontextmanager
import models
import schemas


# create db tables on start
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="CICD Demo API",
    description="CICD Demo to-do list API built with FastAPI and PostgreSQL",
    version="0.1.0",
    lifespan=lifespan
)


# open session and hand it to endpoint function, closes when fin
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# endpoints (CRUD)


@app.get("/")
def root():
    return {"status": "ok", "message": "CICD Demo API", "author": "Kyle Cornford"}


# return all tasks from db
@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Item).all()
    return tasks


# create a new task, add it to db, save to db, and return the id and timestamp
@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Item(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# retrieve and return a single task by id from db, return 404 if not found in db
@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Item).filter(models.Item.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found in db")
    return task


# delete a task by id from db, return 404 if not found in db
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Item).filter(models.Item.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found in db")
    db.delete(task)
    db.commit()
    return None
