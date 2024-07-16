from extensions import Base
from marshmallow import fields, Schema
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref
from datetime import datetime


from .employees import Employee
from .auth import User
from .constraints import Constraint, ConstraintSchema
from .qualifications import Qualification, QualificationSchema
from .tasks import Task, TaskSchema

facility_constraints = Table(
    "facility_constraints",
    Base.metadata,
    Column('facility_id', ForeignKey('facilities.facility_id', ondelete='CASCADE'), primary_key=True),
    Column('constraint_id', ForeignKey('constraints.constraint_id', ondelete='CASCADE'), primary_key=True),
    UniqueConstraint('facility_id', 'constraint_id', name='uq_facility_constraint')
)
facility_qualifications = Table(
    "facility_qualifications",
    Base.metadata,
    Column('facility_id', ForeignKey('facilities.facility_id', ondelete='CASCADE'), primary_key=True),
    Column('qualification_id', ForeignKey('qualifications.qualification_id', ondelete='CASCADE'), primary_key=True),
    UniqueConstraint('facility_id', 'qualification_id', name='uq_facility_qualification')
)

facility_tasks = Table(
    "facility_tasks",
    Base.metadata,
    Column('facility_id', ForeignKey('facilities.facility_id', ondelete='CASCADE')),
    Column('task_id', ForeignKey('tasks.task_id', ondelete='CASCADE')),
    UniqueConstraint('facility_id', 'task_id', name='uq_facility_task')
)


class Facility(Base):
    __tablename__ = 'facilities'
    facility_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(191), nullable=False, unique=True)

    # One to Many
    employees: Mapped[list["Employee"]] = relationship(backref='facility')
    users: Mapped[list["User"]] = relationship(backref='facility', cascade="all, delete-orphan", passive_deletes=True)

    # Many to Many
    constraints: Mapped[list[Constraint]] = relationship(
        secondary=facility_constraints, backref=backref("facilities", passive_deletes=True))
    qualifications: Mapped[list[Qualification]] = relationship(
        secondary=facility_qualifications, backref=backref("facilities", passive_deletes=True))
    tasks: Mapped[list[Task]] = relationship(
        secondary=facility_tasks, backref=backref("facilities", passive_deletes=True))

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)


class FacilitySchema(Schema):

    facility_id = fields.Int()
    name = fields.Str()

    qualifications = fields.Nested(QualificationSchema, many=True)
    constraints = fields.Nested(ConstraintSchema, many=True)
    tasks = fields.Nested(TaskSchema, many=True)
