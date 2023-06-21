from flask import Flask, request, render_template
from db import db, LogEntry, get_entries_by_ip, get_entries_by_date_range, get_grouped_by_ip, get_grouped_by_date, get_all_entries
import json
import os

config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_file_path) as json_data_file:
    config = json.load(json_data_file)

db_url = config['database']['DB_URL']

api_host = config['API']['API_HOST']
api_port = config['API']['API_PORT']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/logs', methods=['GET'])
def get_logs():
    ip = request.args.get('ip')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if ip:
        entries = get_entries_by_ip(ip)
    elif start_date and end_date:
        entries = get_entries_by_date_range(start_date, end_date)
    else:
        entries = get_all_entries()  # Return all entries if no parameters

    return render_template("logs.html", entries=[entry.to_dict() for entry in entries])


@app.route('/logs/grouped', methods=['GET'])
def get_grouped_logs():
    group_by = request.args.get('group_by')
    sort_by = request.args.get('sort_by', 'ip')  # Default sort by 'ip'
    sort_order = request.args.get('sort_order', 'asc')  # Default sort order 'asc'

    if group_by == 'ip':
        entries = get_grouped_by_ip()
    elif group_by == 'date':
        entries = get_grouped_by_date()
    else:
        entries = [entry.to_dict() for entry in get_all_entries()]  # Return all entries if no parameters

    # Sort the entries based on the sorting parameters
    entries = sort_entries(entries, sort_by, sort_order)

    return render_template('grouped_logs.html', entries=entries)


def sort_entries(entries, sort_by, sort_order):
    reverse = False
    if sort_order == 'desc':
        reverse = True

    return sorted(entries, key=lambda entry: entry.get(sort_by, ''), reverse=reverse)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=api_host, port=api_port)
