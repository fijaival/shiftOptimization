from extensions import Base
from datetime import datetime
from marshmallow import Schema, fields
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class EmployeeType(Base):
    __tablename__ = 'employee_types'

    employee_type_id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class EmployeeTypeSchema(Schema):
    employee_type_id = fields.Int()
    type_name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
