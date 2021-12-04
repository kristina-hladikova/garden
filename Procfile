release: python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn Zahradka.wsgi && python manage.py runserver 0.0.0.0:$PORT
