from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import Session
from .import models, schemas, crud
from .database import SessionLocal, engine

app = FastAPI()

task_router = APIRouter(prefix="/shift-tasks", tags=["Tasks"])
product_router = APIRouter(prefix="/products", tags=["Products"])

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@task_router.post("/create")
def post_shift_task(shift_task: schemas.ShiftTaskCreate, db: Session = Depends(get_db)):
    created_task = crud.create_shift_task(shift_task, db)
    return created_task


@task_router.get("/get-{task_id}")
def get_shift_task(task_id: int = Path(..., title="The ID of the shift task to retrieve"),
                    db: Session = Depends(get_db)):
    shift_task = crud.get_shift_task_by_id(db, task_id)

    if not shift_task:
        raise HTTPException(status_code=404, detail="Shift task not found")

    return shift_task


@task_router.put("/update-{task_id}")
def update_shift_task(task_id: int, shift_task_update: schemas.ShiftTaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_shift_task(db, task_id, shift_task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Shift task not found")
    return updated_task


@task_router.get("/filter")
def filter_get_shift_tasks(filters: schemas.ShiftTaskFilter = Depends(), db: Session = Depends(get_db)):
    return crud.filter_shift_tasks(db, filters)


@product_router.post("/create")
def add_products_to_batch(
    products: schemas.ProductListInput,
    db: Session = Depends(get_db)
):
    added_products = crud.add_products(db, products)
    return added_products


@product_router.post("/create-aggregate")
def aggregate_product(
    aggregation_input: schemas.AggregationInput,
    db: Session = Depends(get_db)
):
    product_code = crud.aggregate_product(db, aggregation_input)
    if not product_code:
        raise HTTPException(status_code=404, detail="Product code not found")
    return product_code


app.include_router(task_router)
app.include_router(product_router)
