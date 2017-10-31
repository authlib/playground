import datetime

from sqlalchemy import Column
from sqlalchemy import (
    Integer, String, DateTime, Text
)
from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(80))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class Connect(Base):
    __tablename__ = 'connect'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    app = Column(String(20), nullable=False)
    token_type = Column(String(20))
    access_token = Column(String(48), nullable=False)
    refresh_token = Column(String(48))
    extras = Column(Text)
    expires_at = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
