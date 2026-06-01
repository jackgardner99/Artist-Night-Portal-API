web: gunicorn aportalproject.wsgi
release: python manage.py migrate && python manage.py loaddata users && python manage.py loaddata tokens
