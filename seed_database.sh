#!/bin/bash

rm db.sqlite3
rm -rf ./aportalapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations aportalapi
python3 manage.py migrate aportalapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

