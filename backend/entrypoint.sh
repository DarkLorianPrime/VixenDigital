#!/bin/bash
python manage.py migrate
python manage.py init_elastic
python manage.py initialize_buckets
python manage.py runserver 0.0.0.0:8000