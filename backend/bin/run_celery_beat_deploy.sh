#!/bin/bash
# start celery
export DJANGO_SETTINGS_MODULE=backend.settings.deploy
celery -A backend beat --detach
celery -A backend worker -l DEBUG --task-events --uid=nobody --gid=nogroup --concurrency=1
