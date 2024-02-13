"""
Create SQLAlchemy Tables
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from my_api.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    date_modified = Column(DateTime, default=datetime.datetime.utcnow())
    is_deleted = Column(Boolean, default=False)
