from extensions import Base
from marshmallow import fields, Schema

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Qualification(Base):
    __tablename__ = 'qualifications'

    qualification_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=datetime.now, onupdate=datetime.now)


class QualificationSchema(Schema):
    qualification_id = fields.Int()
    name = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
