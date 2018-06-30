#!/bin/bash

python manage.py migrate --noinput
python manage.py makemessages -a
python manage.py collectstatic --noinput

exec "$@"
