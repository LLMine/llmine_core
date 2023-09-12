#!/bin/bash
gunicorn --workers 3 --bind 0.0.0.0:8000 --timeout 120 llmine_core.wsgi:application