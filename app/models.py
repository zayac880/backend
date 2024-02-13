from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ShiftTaskDB(Base):
    __tablename__ = "shift_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Boolean)
    task_description = Column(String)
    workshop = Column(String)
    shift = Column(String)
    brigade = Column(String)
    batch_number = Column(Integer)
    batch_date = Column(Date)
    product = Column(String)
    ecn_code = Column(String)
    rc_identifier = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    product_codes = relationship(
        "ProductCode",
        primaryjoin="ShiftTaskDB.id == ProductCode.shift_task_id",
        back_populates="shift_task"
    )


class ProductCode(Base):
    __tablename__ = "product_codes"

    id = Column(Integer, primary_key=True, index=True)
    shift_task_id = Column(Integer, ForeignKey("shift_tasks.id"))
    code = Column(String, unique=True, index=True)
    batch_number = Column(Integer)
    batch_date = Column(Date)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime, nullable=True)

    shift_task = relationship(
        "ShiftTaskDB",
        foreign_keys=[shift_task_id],
        back_populates="product_codes"
    )
