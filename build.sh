#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('user', '', 'user12345') if not User.objects.filter(username='user').exists() else None"