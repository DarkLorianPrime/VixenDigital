#!/bin/bash
python manage.py migrate
python manage.py init_elastic
python manage.py initialize_buckets
if [ "$TEST" == "true" ]; then
python manage.py test
else
python manage.py runserver 0.0.0.0:8000
fi
