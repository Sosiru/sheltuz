#!/bin/bash

python manage.py collectstatic --no-input

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --timeout 300 \
    sheltuz.wsgi:application -w 2
