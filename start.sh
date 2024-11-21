#!/bin/bash

# Start MySQL server
service mysql start

# Set up MySQL database and user
mysql -u root -e "CREATE DATABASE IF NOT EXISTS student_details;"
mysql -u root -e "CREATE USER IF NOT EXISTS 'supreme_leader'@'%' IDENTIFIED BY 'A!@#$%^123456';"
mysql -u root -e "GRANT ALL PRIVILEGES ON student_details.* TO 'supreme_leader'@'%';"
mysql -u root -e "FLUSH PRIVILEGES;"

# Run Django migrations
python manage.py migrate

# Start Django server
exec python manage.py runserver 0.0.0.0:10000
