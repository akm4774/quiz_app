#!/bin/bash

# Wait for the database to be ready
/wait-for-it.sh ${DB_HOST}:${DB_PORT} --timeout=30 --strict

# Run Django migrations
python manage.py migrate

# Start Django server
exec python manage.py runserver 0.0.0.0:10000
