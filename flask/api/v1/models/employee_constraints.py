from extensions import Base
from marshmallow import Schema, fields
from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .constraints import Constraint, ConstraintSchema


class EmployeeConstraint(Base):
    __tablename__ = 'employee_constraints'

    employee_id: Mapped[int] = mapped_column(ForeignKey(
        'employees.employee_id', ondelete="CASCADE"), primary_key=True)
    constraint_id: Mapped[int] = mapped_column(ForeignKey(
        'constraints.constraint_id', ondelete="CASCADE"),  primary_key=True)
    value: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    constraint: Mapped["Constraint"] = relationship(backref='employee_constraints')

    __table_args__ = (
        UniqueConstraint('employee_id', 'constraint_id', name='uq_employee_constraint'),
    )


class EmployeeConstraintSchema(Schema):
    employee_id = fields.Int()
    constraint_id = fields.Int()
    value = fields.Int()

    constraint = fields.Nested(ConstraintSchema, only=('constraint_id', 'name'))
