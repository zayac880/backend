from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shift-tasks/")
def post_shift_task(shift_task: schemas.ShiftTaskCreate, db: Session = Depends(get_db)):
    created_task = crud.create_shift_task(shift_task, db)
    return created_task

