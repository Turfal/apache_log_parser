# Парсер Apache-логов

Это приложение на Python для парсинга файлов журнала доступа Apache и сохранения извлеченных данных в базе данных MySQL. Для взаимодействия с базой данных используются Flask и SQLAlchemy. Это приложение разработано в рамках тестового задания.

## Возможности

- Парсит файлы журнала доступа Apache и извлекает необходимую информацию, такую как IP-адрес, дата, HTTP-метод, ресурс, протокол, код состояния и размер.
- Сохраняет извлеченные записи журнала в базе данных MySQL.
- Предоставляет различные методы запросов для получения записей журнала и генерации отчетов по IP-адресам и датам.
- Включает веб-сервер Flask для обслуживания данных журнала и отображения отчетов.

## Требования

- Python 3.x
- Flask
- Flask-SQLAlchemy
- PyMySQL

## Установка

1. Клонируйте репозиторий:

   ```shell
   git clone https://github.com/your-username/apache-log-parser.git
   ```
   
2. Перейдите в каталог проекта:
   cd apache-log-parser

3. Создайте виртуальное окружение (опционально, но рекомендуется):
   python -m venv venv

4. Активируйте виртуальное окружение:
   - В Windows:
     venv\Scripts\activate

   - В macOS и Linux:
     source venv/bin/activate

5. Установите необходимые зависимости:
     pip install -r requirements.txt

6. Настройте базу данных:
    Откройте файл app/db.py и обновите переменную SQLALCHEMY_DATABASE_URI с данными подключения к вашей базе данных MySQL.

7. Запустите приложение:
    python app/api.py

## Использование

1. Разместите файлы журнала доступа Apache в каталоге logs.

2. Запустите приложение для парсинга файлов журнала и сохранения данных в базе данных.
   - python app/parser.py

3. Используйте предоставленные методы запросов в app/db.py для получения записей журнала и генерации отчетов по IP-адресам и датам.

4. Чтобы просмотреть отчеты и взаимодействовать с данными журнала, запустите веб-сервер Flask:
   - python app/server.py

   Откройте веб-браузер и перейдите по адресу http://localhost:5000/logs, чтобы получить доступ к веб-интерфейсу.
   -Сортировка по ip и колличеству находится по адресу http://localhost:5000/logs/grouped (Чтобы отсортировать, необходимо нажать на интересующий вас пункт 'ip' или 'count'), (Чтобы получить данные сгрупированные по 'ip' в формате json, необходимо указать в конце ссыллки "&format=json")
   -Пример ссылки для получения данных в формате json (http://localhost:5000/logs/grouped?group_by=ip&format=json)
   
