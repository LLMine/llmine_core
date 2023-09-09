#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn --workers 3 --bind 0.0.0.0:8000 --timeout 120 llmine_core.wsgi:application