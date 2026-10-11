web: python manage.py migrate && python manage.py loaddata users && python manage.py loaddata tokens && gunicorn aportalproject.wsgi --workers 2 --threads 4 --timeout 120
