![image](https://github.com/Turfal/apache_log_parser/assets/130888083/294b324b-9ec4-4569-ab71-c1bac2eca9c1)

# Парсер Apache-логов

Для взаимодействия с базой данных используются Flask и SQLAlchemy. Это приложение разработано в рамках тестового задания.

## Возможности

- Парсит файлы журнала доступа Apache и извлекает необходимую информацию, такую как IP-адрес, дата, HTTP-метод, ресурс, протокол, код состояния и размер.
- Сохраняет извлеченные записи журнала в базе данных MySQL.
- Предоставляет различные методы запросов для получения записей журнала и генерации отчетов по IP-адресам и датам.
- Включает веб-сервер Flask для обслуживания данных журнала и отображения отчетов.
- Получение данных в формате json.
- Сортировка по IP, Date, Count.

## Требования

- Python 3.x
- Flask
- Flask-SQLAlchemy
- PyMySQL

## Установка

1. Клонируйте репозиторий:

   ```shell
   git clone https://github.com/Turfal/apache-log-parser.git
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

   Откройте веб-браузер и перейдите по адресу http://localhost:5000/, чтобы получить доступ к веб-интерфейсу.
   ![image](https://github.com/Turfal/apache_log_parser/assets/130888083/3c27111e-ddb5-4609-a9d1-ccbae9e299f8)
   
   -Сортировка по ip и колличеству находится по адресу http://localhost:5000/logs/grouped (Чтобы отсортировать, необходимо нажать на интересующий вас пункт 'ip' или 'count')
   ![image](https://github.com/Turfal/apache_log_parser/assets/130888083/b7bf7c4a-623d-48fa-80b5-e55012e0dd58)
   
   -Чтобы получить данные в формате json, на главной странице нажать на соответствующий пункт 'Logs as JSON'
   
   -Пример ссылки для получения данных в формате json (http://localhost:5000/logs/grouped/json)
   ![image](https://github.com/Turfal/apache_log_parser/assets/130888083/60ac6d14-9767-443c-8610-2afd4a5a1bc7)
   
   ![image](https://github.com/Turfal/apache_log_parser/assets/130888083/51f7ec8e-348d-4f36-880f-e357dca1df5e)
   
   ![image](https://github.com/Turfal/apache_log_parser/assets/130888083/961d097f-99d1-4c50-b22c-45d1c930de7c)


   
