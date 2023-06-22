from flask import Flask, request, jsonify, render_template
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='Страница не найдена'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error='Внутренняя ошибка сервера'), 500

@app.errorhandler(Exception)
def general_error(error):
    app.logger.exception(error)
    return render_template('error.html', error='Произошла ошибка'), 500

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        ip = request.args.get('ip')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if ip:
            entries = get_entries_by_ip(ip)
        elif start_date and end_date:
            entries = get_entries_by_date_range(start_date, end_date)
        else:
            entries = LogEntry.query.all()

        if request.args.get('format') == 'json':
            return jsonify(entries=[entry.to_dict() for entry in entries])
        else:
            return render_template("logs.html", entries=[entry.to_dict() for entry in entries])
    except Exception as e:
        app.logger.exception(e)
        return render_template('error.html', error='Произошла ошибка'), 500

@app.route('/logs/grouped', methods=['GET'])
def get_grouped_logs():
    group_by = request.args.get('group_by', default='ip', type=str)
    sort_by = request.args.get('sort_by', default='ip', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)

    if group_by == 'ip':
        entries = get_grouped_by_ip()
    elif group_by == 'date':
        entries = get_grouped_by_date()
    else:
        return "Invalid group_by parameter", 400

    entries = sort_entries(entries, sort_by, sort_order)

    return render_template('grouped_logs.html', entries=entries, sort_order='desc' if sort_order == 'asc' else 'asc')

@app.route('/logs/grouped/json', methods=['GET'])
def get_grouped_logs_json():
    group_by = request.args.get('group_by', default='ip', type=str)
    sort_by = request.args.get('sort_by', default='ip', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)

    if group_by == 'ip':
        entries = get_grouped_by_ip()
    elif group_by == 'date':
        entries = get_grouped_by_date()
    else:
        return "Invalid group_by parameter", 400

    entries = sort_entries(entries, sort_by, sort_order)

    return jsonify(entries=entries)

def sort_entries(entries, sort_by, sort_order):
    reverse = False
    if sort_order == 'desc':
        reverse = True

    return sorted(entries, key=lambda entry: entry.get(sort_by, ''), reverse=reverse)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=api_host, port=api_port)
