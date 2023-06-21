from db import db
from sqlalchemy import func
from models import LogEntry
  # assuming your LogEntry model is in a file named models.py

def get_entries_by_ip(ip):
    return LogEntry.query.filter_by(ip=ip).all()

def get_entries_by_date_range(start_date, end_date):
    return LogEntry.query.filter(LogEntry.date.between(start_date, end_date)).all()

def get_grouped_by_ip():
    return db.session.query(LogEntry.ip_address, func.count(LogEntry.ip_address)).group_by(LogEntry.ip_address).all()

def get_grouped_by_date():
    return db.session.query(func.date(LogEntry.date), func.count(func.date(LogEntry.date))).group_by(func.date(LogEntry.date)).all()
