#!/bin/bash

python manage.py migrate
python manage.py init_elastic
python manage.py initialize_buckets

echo "FTG_TEST: $TEST"

apt-get -y update;
apt-get -y install curl
until curl http://elk:9200; do
  echo "not working..."
  sleep 1
done

if [ "$TEST" == "true" ]; then
  python manage.py test
else
  python manage.py runserver 0.0.0.0:8000
fi
