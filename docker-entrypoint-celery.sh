#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --no-input --email admin@example.com
celery -A llmine_core worker -l info --concurrency=2
