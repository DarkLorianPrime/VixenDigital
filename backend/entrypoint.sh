#!/bin/bash

apt-get -y update;
apt-get -y install curl

python manage.py migrate
python manage.py init_elastic
python manage.py initialize_buckets

python manage.py runserver 0.0.0.0:8000

