from fastapi import FastAPI, Depends, HTTPException, Path
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


@app.get("/shift-tasks/{task_id}")
def get_shift_task(task_id: int = Path(..., title="The ID of the shift task to retrieve"),
                    db: Session = Depends(get_db)):
    shift_task = crud.get_shift_task_by_id(db, task_id)

    if not shift_task:
        raise HTTPException(status_code=404, detail="Shift task not found")

    return shift_task

