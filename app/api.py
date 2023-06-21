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

# Обработчик исключения 404 - страница не найдена
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error='Страница не найдена'), 404

# Обработчик исключения 500 - внутренняя ошибка сервера
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error='Внутренняя ошибка сервера'), 500

# Обработчик исключения общего типа
@app.errorhandler(Exception)
def general_error(error):
    app.logger.exception(error)
    return render_template('error.html', error='Произошла ошибка'), 500

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
            entries = LogEntry.query.all()  # Получить все записи, если нет параметров

        if request.args.get('format') == 'json':
            return jsonify(entries=[entry.to_dict() for entry in entries])
        else:
            return render_template("logs.html", entries=[entry.to_dict() for entry in entries])
    except Exception as e:
        app.logger.exception(e)
        return render_template('error.html', error='Произошла ошибка'), 500



@app.route('/logs/grouped', methods=['GET'])
def get_grouped_logs():
    try:
        group_by = request.args.get('group_by')
        format_type = request.args.get('format', 'html')  # Формат по умолчанию HTML

        if group_by == 'ip':
            entries = get_grouped_by_ip()
        else:
            entries = []  # Вернуть пустой список, если нет параметров

        if format_type == 'json':
            return jsonify(entries)

        return render_template('grouped_logs.html', entries=entries)
    except Exception as e:
        app.logger.exception(e)
        return render_template('error.html', error='Произошла ошибка'), 500


def sort_entries(entries, sort_by, sort_order):
    reverse = False
    if sort_order == 'desc':
        reverse = True

    return sorted(entries, key=lambda entry: entry.get(sort_by, ''), reverse=reverse)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host=api_host, port=api_port)
