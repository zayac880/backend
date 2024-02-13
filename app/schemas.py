from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional


class ShiftTaskCreate(BaseModel):
    status: bool = Field(..., alias="СтатусЗакрытия")
    task_description: str = Field(..., alias="ПредставлениеЗаданияНаСмену")
    workshop: str = Field(..., alias="Рабочий центр")
    shift: str = Field(..., alias="Смена")
    brigade: str = Field(..., alias="Бригада")
    batch_number: int = Field(..., alias="НомерПартии")
    batch_date: date = Field(..., alias="ДатаПартии")
    product: str = Field(..., alias="Номенклатура")
    ecn_code: str = Field(..., alias="КодЕКН")
    rc_identifier: str = Field(..., alias="ИдентификаторРЦ")
    start_time: datetime = Field(..., alias="ДатаВремяНачалаСмены")
    end_time: datetime = Field(..., alias="ДатаВремяОкончанияСмены")
    closed_at: Optional[datetime] = None
    id: Optional[int] = None


class ShiftTaskUpdate(BaseModel):
    status: Optional[bool] = None
    task_description: Optional[str] = None
    workshop: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[datetime] = None
    product: Optional[str] = None
    ecn_code: Optional[str] = None
    rc_identifier: Optional[str] = None


class ShiftTaskFilter(BaseModel):
    status: Optional[bool] = None
    batch_number: Optional[int] = None
    batch_date: Optional[str] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0


class ProductInput(BaseModel):
    unique_product_code: str
    batch_number: int
    batch_date: str


class ProductListInput(BaseModel):
    products: List[ProductInput]
