from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import String, Boolean, DateTime
from uuid import uuid4, UUID
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime] = mapped_column(default=None)

class VerificationCode(Base):
    __tablename__ = "users_email_verification_codes"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(default=lambda: datetime.utcnow() + timedelta(minutes=5))