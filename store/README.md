Это учебный проект по курсу https://stepik.org/course/125859

Проект реализует интернет магазин с каталогом, корзиной, профилем и оплатой(тестовой). На странице каталога реализовано
кеширование с Redis, а в момент регистрации отложенная задача с Celery. Также вне курса добавлена контейнеризация
приложения, кроме базы данных. Она работает на хосте.

Посмотреть проект можно по адресу https://store-server-study.ru/

Стек технологий:

- python = "3.11"
- django = "3.2.13"
- postgresql = "15"
- redis-server = "7.0.11"
- pillow = "9.5.0"
- isort = "5.12.0"
- flake8 = "6.1.0"
- psycopg2-binary = "2.9.7"
- django-allauth = "0.55.2"
- django-debug-toolbar = "4.2.0"
- django-redis = "5.3.0"
- celery = "5.3.4"
- python-dotenv = "1.0.0"
- stripe = "6.3.0"
- django-extensions = "3.2.3"
- djangorestframework = "3.14.0"