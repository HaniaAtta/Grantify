# models/website.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    last_status = Column(String, default="Unknown")
    last_checked = Column(DateTime, default=datetime.utcnow)
