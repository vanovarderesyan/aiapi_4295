release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn pdf_api.wsgi
