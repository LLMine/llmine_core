#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate
celery -A llmine_core worker -l info --concurrency=2
