#!/bin/sh

set -e

echo "Waiting for PostgreSQL to start $DB_HOST:$DB_PORT..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  echo "PostgreSQL is not reachable – sleeping for 1 second"
  sleep 1
done
echo "PostgreSQL is ready – continuing..."

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Running Django collectstatic, migrations, and superuser creation..."

  python manage.py collectstatic --noinput
  python manage.py makemigrations
  python manage.py migrate
  sleep 3
  python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(email=email).exists():
    print(f"Creating superuser '{email}'...")
    User.objects.create_superuser(email=email, password=password)
    print(f"Superuser '{email}' created.")
else:
    print(f"Superuser '{email}' already exists.")
EOF
fi

if [ "$RUN_WORKER" = "true" ]; then
  echo "Waiting for Redis $REDIS_LOCATION..."

  REDIS_HOST=$(echo $REDIS_LOCATION | sed -E 's#redis://([^:]+):([0-9]+)/[0-9]+#\1#')
  REDIS_PORT=$(echo $REDIS_LOCATION | sed -E 's#redis://([^:]+):([0-9]+)/[0-9]+#\2#')

  while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
    echo "Redis is not reachable – sleeping for 1 second"
    sleep 1
  done

  echo "Redis is ready!"
  echo "Starting RQ-Worker..."
  exec python manage.py rqworker default
fi

if [ "$RUN_WORKER" != "true" ]; then
  echo "Starting Gunicorn..."
  exec gunicorn core.wsgi:application \
       --bind 0.0.0.0:8000 \
       --workers 3 \
       --timeout 60
fi