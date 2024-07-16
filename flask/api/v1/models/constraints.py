from extensions import Base
from datetime import datetime


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import Schema, fields


class Constraint(Base):
    __tablename__ = 'constraints'

    constraint_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class ConstraintSchema(Schema):
    constraint_id = fields.Int()
    name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
