from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    date = Column(DateTime)
    request = Column(String)
    status_code = Column(Integer)
    user_agent = Column(String)