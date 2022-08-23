release: python manage.py migrate
web: daphne shopzon.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery:celery -A shopzon.celery worker -l info