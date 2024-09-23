from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, select
from datetime import datetime

from .base import Base
from data.db import get_session

class User(Base):
    __tablename__ = "users"
    
    full_name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))

    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())

    @classmethod
    def row_to_model(cls, pRow: tuple):
        name, hash = pRow 
        return User(name = name, hash = hash)

    @classmethod
    def get_all(cls):
        with get_session() as session:
            try:
                users = session.query(cls).all()
                return users
            except Exception:
                return None

    @classmethod
    def get_one_by_email(cls, pEmail: str):
        query = select(cls).where(cls.email == pEmail)

        with get_session() as session:
            try:
                result = session.execute(query)
                return result.scalars().first()
            except Exception:
                return None