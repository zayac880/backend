from sqlalchemy.orm import Session
from . import models, schemas

from datetime import datetime


def create_shift_task(shift_task: schemas.ShiftTaskCreate, db: Session):
    existing_task = db.query(models.ShiftTaskDB).filter_by(
        batch_number=shift_task.batch_number,
        batch_date=shift_task.batch_date
    ).first()
    if existing_task:
        shift_task_dict = shift_task.dict(exclude={"id"})
        for field, value in shift_task_dict.items():
            setattr(existing_task, field, value)
        db.commit()
        db.refresh(existing_task)
        return existing_task
    else:
        db_shift_task = models.ShiftTaskDB(**shift_task.dict())
        db.add(db_shift_task)
        db.commit()
        db.refresh(db_shift_task)
        return db_shift_task


def get_shift_task_by_id(db: Session, task_id: int):
    return db.query(models.ShiftTaskDB).filter(models.ShiftTaskDB.id == task_id).first()


def update_shift_task(db: Session, task_id: int, shift_task_update: schemas.ShiftTaskUpdate):
    shift_task = db.query(models.ShiftTaskDB).filter(models.ShiftTaskDB.id == task_id).first()
    if not shift_task:
        return None

    for field, value in shift_task_update.dict().items():
        if value is not None:
            if field == "status":
                if value:
                    shift_task.closed_at = datetime.now()
                else:
                    shift_task.closed_at = None
            setattr(shift_task, field, value)

    db.commit()
    db.refresh(shift_task)
    return shift_task
