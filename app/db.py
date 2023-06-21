from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tutnet55@localhost/test'
db = SQLAlchemy(app)

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(2048), nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'date': self.date,
            'method': self.method,
            'resource': self.resource,
            'protocol': self.protocol,
            'status': self.status,
            'size': self.size
        }



def add_entry_to_db(entry):
    db.session.add(entry)
    db.session.commit()

def get_all_entries():
    return LogEntry.query.all()

def get_entries_by_ip(ip):
    return LogEntry.query.filter_by(ip=ip).all()

def get_entries_by_date_range(start_date, end_date):
    return LogEntry.query.filter(LogEntry.date.between(start_date, end_date)).all()

def get_grouped_by_ip():
    result = db.session.query(LogEntry.ip, db.func.count(LogEntry.ip)).group_by(LogEntry.ip).all()
    grouped_entries = [{'ip': entry[0], 'count': entry[1]} for entry in result]
    return grouped_entries

def get_grouped_by_date():
    return db.session.query(db.func.date(LogEntry.date), db.func.count(db.func.date(LogEntry.date))).group_by(db.func.date(LogEntry.date)).all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
