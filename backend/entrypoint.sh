#!/bin/bash
set -ex
exec "$@"

echo "FTG_TEST: $1, $0, $TEST"

apt-get -y update;E
apt-get -y install curl
until curl http://elk:9200; do
  echo "not working..."
  sleep 1
done

python manage.py migrate
python manage.py init_elastic
python manage.py initialize_buckets
echo
if [ "$TEST" = "yes" ]; then
  python manage.py test
else
  python manage.py runserver 0.0.0.0:8000
fi
