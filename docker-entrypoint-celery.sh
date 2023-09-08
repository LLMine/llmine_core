#!/bin/bash
celery -A llmine_core worker -l info --concurrency=2
