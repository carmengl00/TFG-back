#!/bin/bash

# turn on bash's job control
set -m

# clean old data
rm -f celerybeat.pid
rm -f celerybeat-schedule

# collect static files in /static_root
python manage.py collectstatic --noinput

# wait until DB is ready
python manage.py wait_for_db

# DB migrations
python manage.py migrate

# run Django and put it in the background
# python manage.py runserver 0.0.0.0:8000 &

# start uwsgi
uwsgi --ini uwsgi.ini:local --uid=nobody --gid=nogroup --env=DJANGO_SETTINGS_MODULE=backend.settings.local &

# start celery
export DJANGO_SETTINGS_MODULE=backend.settings.local
celery -A backend beat &
celery -A backend worker -E --loglevel=info --uid=nobody --gid=nogroup &

# now we bring the primary process back into the foreground
# and leave it there
fg %1
