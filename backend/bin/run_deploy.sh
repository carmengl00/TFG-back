#!/bin/bash

# turn on bash's job control
set -m

# clean old data
rm -f celerybeat.pid
rm -f celerybeat-schedule

#SET DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=backend.settings.deploy

# collect static files in /static_root
python manage.py collectstatic --noinput

# wait until DB is ready
python manage.py wait_for_db

# DB migrations
python manage.py migrate

#Create Django superuser!
DJANGO_SUPERUSER_PASSWORD=admin_backendback \
DJANGO_SUPERUSER_USER=admin \
DJANGO_SUPERUSER_EMAIL=admin@backend.back \
./manage.py createsuperuser \
--no-input

# run Django and put it in the background
# python manage.py runserver 0.0.0.0:8000 &

# start uwsgi
uwsgi --ini uwsgi.ini:deploy --uid=nobody --gid=nogroup --env=DJANGO_SETTINGS_MODULE=backend.settings.deploy
