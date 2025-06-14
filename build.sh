#!/usr/bin/env bash

echo "Installing npm deps..."
cd theme/static_src
npm install
npm run build
cd ../../

echo "Collecting static files..."
python manage.py collectstatic --noinput
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "Loading fixture data..."
python manage.py loaddata app/fixtures/data.json
