from extensions import Base
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class TaskSchema(Schema):
    task_id = fields.Int()
    name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
