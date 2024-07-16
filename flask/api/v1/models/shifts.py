from extensions import Base
from marshmallow import fields, Schema
from datetime import datetime
from datetime import date as dt_date

from sqlalchemy import String, UniqueConstraint, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column


class Shift(Base):
    __tablename__ = 'shifts'

    shift_id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey(
        'employees.employee_id', ondelete="CASCADE"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey(
        "tasks.task_id", ondelete="CASCADE"), nullable=False)
    date: Mapped[dt_date] = mapped_column(nullable=False)
    shift_number: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('employee_id', 'date', "shift_number", name='uq_shift'),
    )


class ShiftSchema(Schema):
    shift_id = fields.Int()
    employee_id = fields.Int(required=True)
    task_id = fields.Int(required=True)
    date = fields.Date(required=True)
    shift_number = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
