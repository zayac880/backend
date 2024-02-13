from datetime import datetime

from . import models, schemas
from sqlalchemy.orm import Session


def create_shift_task(shift_task: schemas.ShiftTaskCreate, db: Session):
    existing_task = db.query(models.ShiftTaskDB).filter_by(id=shift_task.id).first()
    if existing_task:
        # Обновляем существующую задачу
        shift_task_dict = shift_task.dict(exclude={"id"})
        for field, value in shift_task_dict.items():
            setattr(existing_task, field, value)
        db.commit()
        db.refresh(existing_task)
        return existing_task
    else:
        # Создаем новую задачу с новым id
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


def filter_shift_tasks(db: Session, filters: schemas.ShiftTaskFilter):
    query = db.query(models.ShiftTaskDB)

    if filters.status is not None:
        query = query.filter(models.ShiftTaskDB.status == filters.status)
    if filters.batch_number is not None:
        query = query.filter(models.ShiftTaskDB.batch_number == filters.batch_number)
    if filters.batch_date is not None:
        query = query.filter(models.ShiftTaskDB.batch_date == filters.batch_date)

    query = query.offset(filters.offset).limit(filters.limit)

    return query.all()


def get_product_by_code(db: Session, code: str):
    return db.query(models.ProductCode).filter(models.ProductCode.code == code).first()


def get_shift_task_by_batch_info(db: Session, batch_number: int, batch_date: str):
    return db.query(models.ShiftTaskDB).filter(
        models.ShiftTaskDB.batch_number == batch_number,
        models.ShiftTaskDB.batch_date == batch_date
    ).first()


def add_product_to_shift_task(db: Session, product: schemas.ProductInput, shift_task_id: int):
    new_product = models.ProductCode(
        code=product.unique_product_code,
        batch_number=product.batch_number,
        batch_date=product.batch_date,
        is_aggregated=product.is_aggregated,
        aggregated_at=product.aggregated_at,
        shift_task_id=shift_task_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def add_products(db: Session, products: schemas.ProductListInput):
    added_products = []
    for product_input in products.products:
        shift_task = get_shift_task_by_batch_info(db, product_input.batch_number, product_input.batch_date)
        if shift_task:
            existing_product = get_product_by_code(db, product_input.unique_product_code)
            if existing_product:
                continue
            new_product = models.ProductCode(
                code=product_input.unique_product_code,
                batch_number=product_input.batch_number,
                batch_date=product_input.batch_date,
                is_aggregated=False,
                aggregated_at=None,
                shift_task_id=shift_task.id  # Устанавливаем связь с задачей
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            added_products.append(new_product)
    return added_products


def aggregate_product(db: Session, aggregation_input: schemas.AggregationInput):
    batch = get_shift_task_by_id(db, aggregation_input.shift_tasks_id)
    if not batch:
        return None, "Shift task not found"

    product = get_product_by_code(db, aggregation_input.unique_product_code)
    if not product:
        return None, "Product not found"

    if product.is_aggregated:
        return None, f"Unique code already used at {product.aggregated_at}"

    if product.batch_number != batch.batch_number or product.batch_date != batch.batch_date:
        return None, "Unique code is attached to another batch"

    product.is_aggregated = True
    product.aggregated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product, None
