from datetime import datetime
from extensions import Base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import Schema, fields


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.facility_id', ondelete='CASCADE'), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, facility_id, username, password, is_admin=0):
        self.facility_id = facility_id
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    facility_id = fields.Int(required=True)
    username = fields.Str(required=True)
    is_admin = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    password_hash = fields.Str(load_only=True)
    facility = fields.Nested('FacilitySchema', only=(
        'facility_id', 'name'))


class TokenBlocklist(Base):  # type: ignore
    __tablename__ = 'token_blocklist'
    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
