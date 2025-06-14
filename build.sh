#!/usr/bin/env bash

echo "Installing npm deps..."
cd theme/static_src
npm install
npm run build
cd ../../

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

echo "Loading fixture data..."
python manage.py loaddata fixtures/data.json
