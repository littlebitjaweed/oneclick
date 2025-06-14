#!/usr/bin/env bash

# Install npm dependencies
cd theme/static_src
npm install
npm run build
cd ../../

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Load fixtures
python manage.py loaddata app/fixtures/data.json
